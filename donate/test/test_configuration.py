from ..configuration import parse_config, _required_keys, ConfigurationError
from textwrap import dedent
import pytest


class TestParseYAML:
    yaml_string = dedent("""\
        ---
        total_donation: 20
        split: 4
        currency_symbol: £
        decimal_currency: true

        donees:
          - name: Favourite distro
            weight: critical
            type: disbribution
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

            donees: 5
            """)
        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
        assert "Donees must be a list" == str(e.value)

    def test_invalid_decimal_curreny(self):
        yaml_string = self.yaml_string
        yaml_string = yaml_string.replace("decimal_currency: true",
                                          "decimal_currency: aaa")
        with pytest.raises(ConfigurationError) as e:
            parse_config(yaml_string)
        assert "'decimal_currency' must be a boolean" in str(e.value)
