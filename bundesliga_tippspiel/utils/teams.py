"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bundesliga-tippspiel.

bundesliga-tippspiel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

bundesliga-tippspiel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from typing import Tuple


def get_team_data(team_name: str) -> Tuple[str, str, str, Tuple[str, str]]:
    """
    Generates team short_names, abbreviations and icon URLs for teams
    :param team_name: The team's full name as specified by OpenLigaDB
    :return: A tuple containing the
            name, short_name, abbreviation, svg URL, png URL
    """
    return {
        "1. FC Nürnberg": (
            "1. FC Nürnberg", "1. FC Nürnberg", "FCN",
            wikimedia_icon_urls("commons/f/fa/1._FC_Nürnberg_logo.svg")
        ),
        "1. FSV Mainz 05": (
            "1. FSV Mainz 05", "FSV Mainz 05", "M05",
            wikimedia_icon_urls("commons/0/0b/FSV_Mainz_05_Logo.svg")
        ),
        "Bayer Leverkusen": (
            "Bayer 04 Leverkusen", "Bayer Leverkusen", "B04",
            wikimedia_icon_urls("de/f/f7/Bayer_Leverkusen_Logo.svg")
        ),
        "BV Borussia Dortmund 09": (
            "Borussia Dortmund", "BVB Dortmund", "BVB",
            wikimedia_icon_urls("commons/6/67/Borussia_Dortmund_logo.svg")
        ),
        "Borussia Mönchengladbach": (
            "Borussia Mönchengladbach", "M'Gladbach", "BMG",
            wikimedia_icon_urls("commons/8/81/Borussia_"
                                "Mönchengladbach_logo.svg")
        ),
        "Eintracht Frankfurt": (
            "Eintracht Frankfurt", "Frankfurt", "SGE",
            wikimedia_icon_urls("commons/0/04/Eintracht_Frankfurt_Logo.svg")
        ),
        "FC Augsburg": (
            "FC Augsburg", "FC Augsburg", "FCA",
            wikimedia_icon_urls("de/b/b5/Logo_FC_Augsburg.svg")
        ),
        "FC Bayern": (
            "FC Bayern München", "FC Bayern", "FCB",
            wikimedia_icon_urls("commons/1/1b/"
                                "FC_Bayern_München_logo_(2017).svg")
        ),
        "FC Bayern München": (
            "FC Bayern München", "FC Bayern", "FCB",
            wikimedia_icon_urls("commons/1/1b/"
                                "FC_Bayern_München_logo_(2017).svg")
        ),
        "FC Schalke 04": (
            "FC Schalke 04", "Schalke 04", "S04",
            wikimedia_icon_urls("commons/6/6d/FC_Schalke_04_Logo.svg")
        ),
        "Fortuna Düsseldorf": (
            "Fortuna Düsseldorf", "Düsseldorf", "F95",
            wikimedia_icon_urls("commons/9/94/Fortuna_D%C3%BCsseldorf.svg")
        ),
        "Hannover 96": (
            "Hannover 96", "Hannover 96", "H96",
            wikimedia_icon_urls("commons/c/cd/Hannover_96_Logo.svg")
        ),
        "Hertha BSC": (
            "Hertha BSC Berlin", "Hertha BSC", "BSC",
            wikimedia_icon_urls("commons/8/81/Hertha_BSC_Logo_2012.svg")
        ),
        "RB Leipzig": (
            "RB Leibzig", "RB Leibzig", "RBL",
            wikimedia_icon_urls("it/c/cc/RB_Leipzig_primo_logo.svg")
        ),
        "SC Freiburg": (
            "SC Freiburg", "SC Freiburg", "SCF",
            wikimedia_icon_urls("de/8/88/Logo-SC_Freiburg.svg")
        ),
        "TSG 1899 Hoffenheim": (
            "TSG 1899 Hoffenheim", "TSG Hoffenheim", "TSG",
            wikimedia_icon_urls("commons/e/e7/Logo_TSG_Hoffenheim.svg")
        ),
        "VfB Stuttgart": (
            "VFB Stuttgart", "VFB Stuttgart", "VFB",
            wikimedia_icon_urls("commons/e/eb/VfB_Stuttgart_1893_Logo.svg")
        ),
        "VfL Wolfsburg": (
            "VFL Wolfsburg", "VFL Wolfsburg", "WOB",
            wikimedia_icon_urls("commons/c/ce/VfL_Wolfsburg_Logo.svg")
        ),
        "Werder Bremen": (
            "SV Werder Bremen", "Werder Bremen", "BRE",
            wikimedia_icon_urls("commons/b/be/SV-Werder-Bremen-Logo.svg")
        ),
        "1. FC Union Berlin": (
            "1. FC Union Berlin", "Union Berlin", "FCU",
            wikimedia_icon_urls("commons/4/44/1._FC_Union_Berlin_Logo.svg")
        ),
        "SC Paderborn 07": (
            "SC Paderborn 07", "Paderborn", "SCP",
            wikimedia_icon_urls("en/b/b3/SC_Paderborn_07_logo.svg")
        ),
        "1. FC Köln": (
            "1. FC Köln", "1. FC Köln", "KOE",
            wikimedia_icon_urls("en/5/53/FC_Cologne_logo.svg")
        ),
        "Arminia Bielefeld": (
            "Arminia Bielefeld", "Bielefeld", "DSC",
            wikimedia_icon_urls("en/9/9b/Arminia_Bielefeld_logo.svg")
        ),
        "SpVgg Greuther Fürth": (
            "SpVgg Greuther Fürth", "Greuther Fürth", "SGF",
            wikimedia_icon_urls("de/b/b1/SpVgg_Greuther_Fürth_2017.svg")
        ),
        "VfL Bochum": (
            "VfL Bochum", "VfL Bochum", "BOC",
            wikimedia_icon_urls("commons/7/72/VfL_Bochum_logo.svg")
        ),
        "1. FC Heidenheim 1846": (
            "1. FC Heidenheim", "Heidenheim", "HDH",
            wikimedia_icon_urls("commons/9/9d/1._FC_Heidenheim_1846.svg")
        ),
        "Erzgebirge Aue": (
            "Erzgebirge Aue", "Erzgebirge Aue", "AUE",
            wikimedia_icon_urls("en/9/9e/FC_Erzgebirge_Aue_logo.svg")
        ),
        "FC Hansa Rostock": (
            "FC Hansa Rostock", "Hansa Rostock", "FCH",
            wikimedia_icon_urls("commons/8/8f/F.C._Hansa_Rostock_Logo.svg")
        ),
        "FC Ingolstadt 04": (
            "FC Ingolstadt 04", "FC Ingolstadt", "FCI",
            wikimedia_icon_urls("en/0/0b/FC_Ingolstadt_04_logo.svg")
        ),
        "FC St. Pauli": (
            "FC St. Pauli", "St. Pauli", "STP",
            wikimedia_icon_urls("en/8/8f/FC_St._Pauli_logo_%282018%29.svg")
        ),
        "Hamburger SV": (
            "Hamburger SV", "Hamburger SV", "HSV",
            wikimedia_icon_urls("commons/f/f7/Hamburger_SV_logo.svg")
        ),
        "Holstein Kiel": (
            "Holstein Kiel", "Holstein Kiel", "KIE",
            wikimedia_icon_urls("commons/3/30/Holstein_Kiel_Logo.svg")
        ),
        "Jahn Regensburg": (
            "SSV Jahn Regensburg", "Jahn Regensburg", "SSV",
            wikimedia_icon_urls("commons/3/3d/Jahn_Regensburg_logo2014.svg")
        ),
        "Karlsruher SC": (
            "Karlsruher SC", "Karlsruher SC", "KSC",
            wikimedia_icon_urls("commons/c/c8/Karlsruher_SC_Logo_2.svg")
        ),
        "SG Dynamo Dresden": (
            "SG Dynamo Dresden", "Dynamo Dresden", "SGD",
            wikimedia_icon_urls("en/0/06/Dynamo_Dresden_logo_2011.svg")
        ),
        "SV Darmstadt 98": (
            "SV Darmstadt 98", "SV Darmstadt", "D98",
            wikimedia_icon_urls("en/9/92/SV_Darmstadt_98_logo.svg")
        ),
        "SV Sandhausen": (
            "SV Sandhausen", "SV Sandhausen", "SVS",
            wikimedia_icon_urls("commons/d/d3/SV_Sandhausen.svg")
        )
    }[team_name]


def wikimedia_icon_urls(path: str, png_size: int = 500) -> Tuple[str, str]:
    """
    Generates URL paths to wikimedia-hosted SVG and PNG files
    :param path: The URL path to the SVG file (without the wikimedia part)
    :param png_size: The size of the PNG file
    :return: The URL path to the SVG File, PNG file
    """
    wikimedia = "https://upload.wikimedia.org/wikipedia"
    base, specific = path.split("/", 1)
    svg_filename = path.rsplit("/", 1)[1]

    svg_url = "{}/{}".format(wikimedia, path)
    png_url = "{}/{}/thumb/{}/{}px-{}.png".format(
        wikimedia, base, specific, png_size, svg_filename
    )

    return svg_url, png_url
