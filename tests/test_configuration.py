from donate.configuration import Configuration
from donate.donee import Donee
from textwrap import dedent
from pydantic import ValidationError
import pytest
import yaml


def test_xdg_config_path():
    path = Configuration.xdg_config_path()
    path_string = str(path.absolute())

    assert path_string.split("/")[-1] == "config.yaml"
    assert path_string.split("/")[-2] == "donate"


class TestParseConfig:
    yaml_string = dedent(
        """\
        ---
        total_donation: 20
        split: 4
        currency_symbol: £
        decimal_currency: true
        schedule: ad hoc

        weights:
          critical: 1.0
          large: 0.5
          medium: 0.25
          small: 0.1

        donees:
          - name: Favourite distro
            weight: critical
            category: distribution
            url: distro.com
          - name: Favourite software
            weight: large
            url: software.com
        """
    )

    def test_parse(self):
        config = Configuration.from_str(self.yaml_string)
        assert config.total_donation == 20
        assert len(config.donees) == 2

    @pytest.mark.skipif(
        not hasattr(yaml, "CLoader"),
        reason="yaml module has no attribute 'CLoader'"
    )
    def test_parse_without_cloader(self, monkeypatch):
        monkeypatch.delattr("yaml.CLoader")

        config = Configuration.from_str(self.yaml_string)
        assert config.total_donation == 20
        assert len(config.donees) == 2

    def test_donees(self):
        config = Configuration.from_str(self.yaml_string)
        assert all(isinstance(item, Donee) for item in config.donees)

        expected_donee = Donee(
            name="Favourite distro",
            weight=1.0,
            category="distribution",
            url="distro.com"
        )
        assert config.donees[0] == expected_donee

        expected_donee = Donee(
            name="Favourite software",
            weight=0.5,
            category="other",
            url="software.com"
        )
        assert config.donees[1] == expected_donee

    def test_no_decimal_currency(self):
        yaml_string = self.yaml_string.replace("decimal_currency: true", "")

        config = Configuration.from_str(yaml_string)
        assert config.decimal_currency is False

    def test_no_currency_symbol(self):
        yaml_string = self.yaml_string.replace("currency_symbol: £", "")

        config = Configuration.from_str(yaml_string)
        assert config.currency_symbol == "£"

    def test_no_schedule(self):
        yaml_string = self.yaml_string.replace("schedule: ad hoc", "")

        config = Configuration.from_str(yaml_string)
        assert config.schedule == "ad hoc"

    def test_monthly_schedule(self):
        yaml_string = self.yaml_string.replace(
            "schedule: ad hoc", "schedule: monthly"
        )

        config = Configuration.from_str(yaml_string)
        assert config.schedule == "monthly"

    def test_invalid_schedule(self):
        yaml_string = self.yaml_string.replace("schedule: ad hoc",
                                               "schedule: occasional")

        with pytest.raises(ValidationError) as e:
            Configuration.from_str(yaml_string)
            assert "Schedule 'occasional' is not valid" in str(e.value)

    def test_invalid_weight_name(self):
        yaml_string = self.yaml_string.replace("weight: critical",
                                               "weight: really big")

        with pytest.raises(ValueError) as e:
            Configuration.from_str(yaml_string)
            assert (
                "Weight 'really big' of donee 'Favourite distro' not defined"
                in str(e.value)
            )
