from donate.configuration import (
    parse_config, _required_keys, ConfigurationError, _parse_donee
)
from donate.donee import Donee
from donate.schedule import AdHoc, Monthly
from textwrap import dedent
import pytest
import yaml


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
        config = parse_config(self.yaml_string)
        assert config["total_donation"] == 20
        assert len(config["donees"]) == 2

    @pytest.mark.skipif(
        not hasattr(yaml, "CLoader"),
        reason="yaml module has no attribute 'CLoader'"
    )
    def test_parse_without_cloader(self, monkeypatch):
        monkeypatch.delattr("yaml.CLoader")

        config = parse_config(self.yaml_string)
        assert config["total_donation"] == 20
        assert len(config["donees"]) == 2

    def test_donees(self):
        config = parse_config(self.yaml_string)
        assert type(config["donees"][0]) is Donee

        expected_donee = Donee(
            name="Favourite distro",
            weight=1.0,
            category="distribution",
            donation_url="distro.com"
        )
        assert config["donees"][0] == expected_donee

        expected_donee = Donee(
            name="Favourite software",
            weight=0.5,
            category="other",
            donation_url="software.com"
        )
        assert config["donees"][1] == expected_donee

    def test_invalid_category(self):
        yaml_string = self.yaml_string.replace(
            "category: distribution",
            "category: 5"
        )
        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
            assert (
                "Category '5' of donee 'Favourite distro' is not a string."
                in str(e.value)
            )

    @pytest.mark.parametrize("key", _required_keys)
    def test_missing_key(self, key):
        yaml_string = self.yaml_string.replace(key, "invalid_key")
        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
            assert f"Required key '{key}' not declared" in str(e.value)

    def test_donees_is_list(self):
        yaml_string = dedent(
            """\
            ---
            total_donation: 20
            split: 4
            currency_symbol: £
            decimal_currency: true
            schedule: ad hoc

            donees: 5
            """
        )
        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
            assert "Donees must be a list" == str(e.value)

    def test_invalid_decimal_currency(self):
        yaml_string = self.yaml_string.replace("decimal_currency: true",
                                               "decimal_currency: aaa")
        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
            assert "'decimal_currency' must be a boolean" in str(e.value)

    def test_no_decimal_currency(self):
        yaml_string = self.yaml_string.replace("decimal_currency: true", "")

        config = parse_config(yaml_string)
        assert "decimal_currency" in config.keys()
        assert config["decimal_currency"] is False

    def test_no_currency_symbol(self):
        yaml_string = self.yaml_string.replace("currency_symbol: £", "")

        config = parse_config(yaml_string)
        assert "currency_symbol" in config.keys()
        assert config["currency_symbol"] == "£"

    def test_no_schedule(self):
        yaml_string = self.yaml_string.replace("schedule: ad hoc", "")

        config = parse_config(yaml_string)
        assert "schedule" in config.keys()
        assert isinstance(config["schedule"], AdHoc)

    def test_monthly_schedule(self):
        yaml_string = self.yaml_string.replace("schedule: ad hoc",
                                               "schedule: monthly")

        config = parse_config(yaml_string)
        assert "schedule" in config.keys()
        assert isinstance(config["schedule"], Monthly)

    def test_invalid_schedule(self):
        yaml_string = self.yaml_string.replace("schedule: ad hoc",
                                               "schedule: occasional")

        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
            assert "Schedule must be one of" in str(e.value)

    def test_no_weights(self):
        yaml_string = self.yaml_string.replace(
            "weights:\n  critical: 1.0\n  large: 0.5\n  medium: 0.25"
            "\n  small: 0.1",
            ""
        )
        yaml_string = yaml_string.replace("weight: critical", "weight: 1")
        yaml_string = yaml_string.replace("weight: large", "weight: 1")

        config = parse_config(yaml_string)
        assert "weights" not in config.keys()

    def test_no_weights2(self):
        yaml_string = self.yaml_string.replace(
            "weights:\n  critical: 1.0\n  large: 0.5\n  medium: 0.25"
            "\n  small: 0.1",
            ""
        )

        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
            exception_message = (
                "The weight of donee 'Favourite distro' is a string, but"
                " no weights have been defined."
            )
            assert str(e.value) == exception_message

    def test_invalid_weight_type(self):
        yaml_string = self.yaml_string.replace("critical: 1.0",
                                               "critical: abc")

        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
            exception_string = (
                "Weight 'critical' value 'abc' is not a real number."
            )
            assert exception_string in str(e.value)

    def test_negative_weight_value(self):
        yaml_string = self.yaml_string.replace("critical: 1.0",
                                               "critical: -2.5")

        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
            exception_string = "Weight 'critical' value '-2.5' is negative."
            assert exception_string in str(e.value)


@pytest.fixture()
def donee_dict():
    donee_dict = {
        "name": "Favourite distro",
        "weight": "critical",
        "category": "Distribution",
        "url": "distro.com"
    }
    return donee_dict


@pytest.fixture()
def weights_dict():
    weights_dict = {
        "critical": 1.0,
        "large": 0.5,
        "medium": 0.25,
        "small": 0.1
    }
    return weights_dict


class TestParseDonee:
    def test_parse(self, donee_dict, weights_dict):
        donee = _parse_donee(donee_dict, weights_dict)
        assert isinstance(donee, Donee)
        assert donee.name == donee_dict["name"]
        assert donee.weight == weights_dict[donee_dict["weight"]]
        assert donee.category == donee_dict["category"].lower()
        assert donee.donation_url == donee_dict["url"]

    def test_invalid_weight_name(self, donee_dict, weights_dict):
        donee_dict["weight"] = "huge"

        with pytest.raises(ConfigurationError) as e:
            _parse_donee(donee_dict, weights_dict)

        exception_message = (
            f"Weight 'huge' of donee '{donee_dict['name']}' not defined"
        )
        assert str(e.value) == exception_message

    def test_missing_weights(self, donee_dict):
        with pytest.raises(ConfigurationError) as e:
            _parse_donee(donee_dict, None)
            exception_message = (
                f"The weight of donee '{donee_dict['name']}' is a string, but"
                " no weights have been defined."
            )
            assert str(e.value) == exception_message

    @pytest.mark.parametrize("weight,expected", [(5, 5.0), (7.0, 7.0)])
    def test_manual_weights(self, donee_dict, weight, expected):
        donee_dict["weight"] = weight

        donee = _parse_donee(donee_dict, None)
        assert type(donee.weight) is float
        assert donee.weight == expected

    def test_negative_weight(self, donee_dict):
        donee_dict["weight"] = -5

        with pytest.raises(ConfigurationError) as e:
            _parse_donee(donee_dict, None)

        exception_message = (
            f"Weight '{float(-5)}' of donee '{donee_dict['name']}' is negative"
        )
        assert str(e.value) == exception_message
