from donate.__main__ import format_donations
import re


def test_format_donations(donations):
    donation_text = format_donations(donations, "$", False)

    assert re.search(r"^Favourite distro\s+\$100\s+distro.com", donation_text,
                     re.MULTILINE)
    assert re.search(r"^Favourite software\s+\$50\s+software.com",
                     donation_text,
                     re.MULTILINE)
    assert re.search(r"^Podcast 1\s+\$10\s+podcast1.com", donation_text,
                     re.MULTILINE)


def test_format_donations2(donations):
    donation_text = format_donations(donations, "£", True)

    assert re.search(r"^Favourite distro\s+\£1.00\s+distro.com", donation_text,
                     re.MULTILINE)
    assert re.search(r"^Favourite software\s+\£0.50\s+software.com",
                     donation_text,
                     re.MULTILINE)
    assert re.search(r"^Podcast 1\s+\£0.10\s+podcast1.com", donation_text,
                     re.MULTILINE)
