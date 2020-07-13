from donate.configuration import (
    parse_config, _required_keys, ConfigurationError
    )
from donate.donee import Donee, Type
from donate.schedule import AdHoc, Monthly
from textwrap import dedent
import pytest
import yaml


class TestParseYAML:
    yaml_string = dedent("""\
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
            type: distribution
            url: distro.com
          - name: Favourite software
            weight: large
            type: software
            url: software.com
        """)

    def test_parse(self):
        config = parse_config(self.yaml_string)
        assert config["total_donation"] == 20
        assert len(config["donees"]) == 2

    @pytest.mark.skipif(
        not hasattr(yaml, "CLoader"),
        reason="yaml module has no attribute 'CLoader'"
        )
    def test_parse_without_cloader(self, monkeypatch):
        yaml_string = self.yaml_string

        monkeypatch.delattr("yaml.CLoader")

        config = parse_config(yaml_string)
        assert config["total_donation"] == 20
        assert len(config["donees"]) == 2

    def test_donees(self):
        config = parse_config(self.yaml_string)
        assert type(config["donees"][0]) is Donee

        expected_donee = Donee(
            name="Favourite distro",
            weight=1.0,
            donee_type=Type.DISTRIBUTION,
            donation_url="distro.com"
            )
        assert config["donees"][0] == expected_donee

    @pytest.mark.parametrize("key", _required_keys)
    def test_missing_key(self, key):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace(key, "invalid_key")
        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
        assert f"Required key '{key}' not declared" in str(e.value)

    def test_donees_is_list(self):
        yaml_string = dedent("""\
            ---
            total_donation: 20
            split: 4
            currency_symbol: £
            decimal_currency: true
            schedule: ad hoc

            donees: 5
            """)
        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
        assert "Donees must be a list" == str(e.value)

    def test_invalid_decimal_currency(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace("decimal_currency: true",
                                          "decimal_currency: aaa")
        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
        assert "'decimal_currency' must be a boolean" in str(e.value)

    def test_no_decimal_currency(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace("decimal_currency: true", "")

        config = parse_config(yaml_string)
        assert "decimal_currency" in config.keys()
        assert config["decimal_currency"] is False

    def test_no_currency_symbol(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace("currency_symbol: £", "")

        config = parse_config(yaml_string)
        assert "currency_symbol" in config.keys()
        assert config["currency_symbol"] == "£"

    def test_no_schedule(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace("schedule: ad hoc", "")

        config = parse_config(yaml_string)
        assert "schedule" in config.keys()
        assert isinstance(config["schedule"], AdHoc)

    def test_monthly_schedule(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace("schedule: ad hoc",
                                          "schedule: monthly")

        config = parse_config(yaml_string)
        assert "schedule" in config.keys()
        assert isinstance(config["schedule"], Monthly)

    def test_invalid_schedule(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace("schedule: ad hoc",
                                          "schedule: occasional")

        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
        assert "Schedule must be one of" in str(e.value)

    def test_no_weights(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace(
            "weights:\n  critical: 1.0\n  large: 0.5\n  medium: 0.25"
            "\n  small: 0.1",
            ""
            )
        yaml_string = yaml_string.replace("weight: critical", "weight: 1")
        yaml_string = yaml_string.replace("weight: large", "weight: 1")

        config = parse_config(yaml_string)
        assert "weights" not in config.keys()

    def test_invalid_weight_type(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace("critical: 1.0", "critical: abc")

        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
        exception_string = (
            "Weight 'critical' value 'abc' is not a real number."
            )
        assert exception_string in str(e.value)

    def test_negative_weight_value(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace("critical: 1.0", "critical: -2.5")

        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
        exception_string = "Weight 'critical' value '-2.5' is negative."
        assert exception_string in str(e.value)
