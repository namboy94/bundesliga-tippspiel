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
    # Tuples: abbrv: openligadb name, full name, short name, logos
    team_map = {
        "FCN": (
            "1. FC Nürnberg", "1. FC Nürnberg", "1. FC Nürnberg",
            wikimedia_icon_urls("commons/f/fa/1._FC_Nürnberg_logo.svg")
        ),
        "M05": (
            "1. FSV Mainz 05", "1. FSV Mainz 05", "FSV Mainz 05",
            wikimedia_icon_urls("commons/0/0b/FSV_Mainz_05_Logo.svg")
        ),
        "B04": (
            "Bayer Leverkusen", "Bayer 04 Leverkusen", "Bayer Leverkusen",
            wikimedia_icon_urls("de/f/f7/Bayer_Leverkusen_Logo.svg")
        ),
        "BVB": (
            "Borussia Dortmund", "Borussia Dortmund", "BVB Dortmund",
            wikimedia_icon_urls("commons/6/67/Borussia_Dortmund_logo.svg")
        ),
        "BMG": (
            "Borussia Mönchengladbach", "Borussia Mönchengladbach",
            "M'Gladbach", wikimedia_icon_urls("commons/8/81/Borussia_"
                                              "Mönchengladbach_logo.svg")
        ),
        "SGE": (
            "Eintracht Frankfurt", "Eintracht Frankfurt", "Frankfurt",
            wikimedia_icon_urls("commons/0/04/Eintracht_Frankfurt_Logo.svg")
        ),
        "FCA": (
            "FC Augsburg", "FC Augsburg", "FC Augsburg",
            wikimedia_icon_urls("de/b/b5/Logo_FC_Augsburg.svg")
        ),
        "FCB": (
            "FC Bayern München", "FC Bayern München", "FC Bayern",
            wikimedia_icon_urls("commons/1/1b/"
                                "FC_Bayern_München_logo_(2017).svg")
        ),
        "S04": (
            "FC Schalke 04", "FC Schalke 04", "Schalke 04",
            wikimedia_icon_urls("commons/6/6d/FC_Schalke_04_Logo.svg")
        ),
        "F95": (
            "Fortuna Düsseldorf", "Fortuna Düsseldorf", "Düsseldorf",
            wikimedia_icon_urls("commons/9/94/Fortuna_D%C3%BCsseldorf.svg")
        ),
        "H96": (
            "Hannover 96", "Hannover 96", "Hannover 96",
            wikimedia_icon_urls("commons/c/cd/Hannover_96_Logo.svg")
        ),
        "BSC": (
            "Hertha BSC", "Hertha BSC Berlin", "Hertha BSC",
            wikimedia_icon_urls("commons/8/81/Hertha_BSC_Logo_2012.svg")
        ),
        "RBL": (
            "RB Leipzig", "RB Leibzig", "RB Leibzig",
            wikimedia_icon_urls("it/c/cc/RB_Leipzig_primo_logo.svg")
        ),
        "SCF": (
            "SC Freiburg", "SC Freiburg", "SC Freiburg",
            wikimedia_icon_urls("de/8/88/Logo-SC_Freiburg.svg")
        ),
        "TSG": (
            "TSG 1899 Hoffenheim", "TSG 1899 Hoffenheim", "TSG Hoffenheim",
            wikimedia_icon_urls("commons/e/e7/Logo_TSG_Hoffenheim.svg")
        ),
        "VFB": (
            "VfB Stuttgart", "VFB Stuttgart", "VFB Stuttgart",
            wikimedia_icon_urls("commons/e/eb/VfB_Stuttgart_1893_Logo.svg")
        ),
        "WOB": (
            "VfL Wolfsburg", "VFL Wolfsburg", "VFL Wolfsburg",
            wikimedia_icon_urls("commons/c/ce/VfL_Wolfsburg_Logo.svg")
        ),
        "BRE": (
            "Werder Bremen", "SV Werder Bremen", "Werder Bremen",
            wikimedia_icon_urls("commons/b/be/SV-Werder-Bremen-Logo.svg")
        ),
        "FCU": (
            "1. FC Union Berlin", "1. FC Union Berlin", "Union Berlin",
            wikimedia_icon_urls("commons/4/44/1._FC_Union_Berlin_Logo.svg")
        ),
        "SCP": (
            "SC Paderborn 07", "SC Paderborn 07", "Paderborn",
            wikimedia_icon_urls("en/b/b3/SC_Paderborn_07_logo.svg")
        ),
        "KOE": (
            "1. FC Köln", "1. FC Köln", "1. FC Köln",
            wikimedia_icon_urls("en/5/53/FC_Cologne_logo.svg")
        ),
        "DSC": (
            "Arminia Bielefeld", "Arminia Bielefeld", "Bielefeld",
            wikimedia_icon_urls("en/9/9b/Arminia_Bielefeld_logo.svg")
        ),
        "SGF": (
            "SpVgg Greuther Fürth", "SpVgg Greuther Fürth", "Greuther Fürth",
            wikimedia_icon_urls("de/b/b1/SpVgg_Greuther_Fürth_2017.svg")
        ),
        "BOC": (
            "VfL Bochum", "VfL Bochum", "VfL Bochum",
            wikimedia_icon_urls("commons/7/72/VfL_Bochum_logo.svg")
        ),
        "HDH": (
            "1. FC Heidenheim 1846", "1. FC Heidenheim", "Heidenheim",
            wikimedia_icon_urls("commons/9/9d/1._FC_Heidenheim_1846.svg")
        ),
        "AUE": (
            "Erzgebirge Aue", "Erzgebirge Aue", "Erzgebirge Aue",
            wikimedia_icon_urls("en/9/9e/FC_Erzgebirge_Aue_logo.svg")
        ),
        "FCH": (
            "FC Hansa Rostock", "FC Hansa Rostock", "Hansa Rostock",
            wikimedia_icon_urls("commons/8/8f/F.C._Hansa_Rostock_Logo.svg")
        ),
        "FCI": (
            "FC Ingolstadt 04", "FC Ingolstadt 04", "FC Ingolstadt",
            wikimedia_icon_urls("en/0/0b/FC_Ingolstadt_04_logo.svg")
        ),
        "STP": (
            "FC St. Pauli", "FC St. Pauli", "St. Pauli",
            wikimedia_icon_urls("en/8/8f/FC_St._Pauli_logo_%282018%29.svg")
        ),
        "HSV": (
            "Hamburger SV", "Hamburger SV", "Hamburger SV",
            wikimedia_icon_urls("commons/f/f7/Hamburger_SV_logo.svg")
        ),
        "KIE": (
            "Holstein Kiel", "Holstein Kiel", "Holstein Kiel",
            wikimedia_icon_urls("commons/3/30/Holstein_Kiel_Logo.svg")
        ),
        "SSV": (
            "Jahn Regensburg", "SSV Jahn Regensburg", "Jahn Regensburg",
            wikimedia_icon_urls("commons/3/3d/Jahn_Regensburg_logo2014.svg")
        ),
        "KSC": (
            "Karlsruher SC", "Karlsruher SC", "Karlsruher SC",
            wikimedia_icon_urls("commons/c/c8/Karlsruher_SC_Logo_2.svg")
        ),
        "SGD": (
            "SG Dynamo Dresden", "SG Dynamo Dresden", "Dynamo Dresden",
            wikimedia_icon_urls("en/0/06/Dynamo_Dresden_logo_2011.svg")
        ),
        "D98": (
            "SV Darmstadt 98", "SV Darmstadt 98", "SV Darmstadt",
            wikimedia_icon_urls("en/9/92/SV_Darmstadt_98_logo.svg")
        ),
        "SVS": (
            "SV Sandhausen", "SV Sandhausen", "SV Sandhausen",
            wikimedia_icon_urls("commons/d/d3/SV_Sandhausen.svg")
        ),
        "FCK": (
            "1. FC Kaiserslautern", "1. FC Kaiserslautern", "Kaiserslautern",
            wikimedia_icon_urls("commons/d/d3/Logo_1_FC_Kaiserslautern.svg")
        ),
        "FCM": (
            "1. FC Magdeburg", "1. FC Magdeburg", "Magdeburg",
            wikimedia_icon_urls("commons/8/84/1._FC_Magdeburg.svg")
        ),
        "FCS": (
            "1. FC Saarbrücken", "1. FC Saarbrücken", "Saarbrücken",
            wikimedia_icon_urls("de/f/ff/1._FC_Saarbr%C3%BCcken.svg")
        ),
        "BRA": (
            "Eintracht Braunschweig", "Eintracht Braunschweig", "Braunschweig",
            wikimedia_icon_urls("de/4/45/Logo_Eintracht_Braunschweig.svg")
        ),
        "VBE": (
            "FC Viktoria 1889 Berlin", "FC Viktoria Berlin", "Viktoria Berlin",
            wikimedia_icon_urls(
                "commons/4/40/FC_Viktoria_1889_Berlin_Logo.svg")
        ),
        "VKO": (
            "FC Viktoria Köln", "FC Viktoria Köln", "Viktoria Köln",
            wikimedia_icon_urls(
                "commons/d/dc/FC_Viktoria_K%C3%B6ln_1904_Logo.svg")
        ),
        "HFC": (
            "Hallescher FC", "Hallescher FC", "Halle",
            wikimedia_icon_urls("commons/e/e1/Hallescher_FC.svg")
        ),
        "MSV": (
            "MSV Duisburg", "MSV Duisburg", "Duisburg",
            wikimedia_icon_urls("commons/0/02/Msv_duisburg_%282017%29.svg")
        ),
        "SC2": (
            "SC Freiburg II", "SC Freiburg II", "Freiburg II",
            wikimedia_icon_urls("de/8/88/Logo-SC_Freiburg.svg")
        ),
        "SCV": (
            "SC Verl", "SC Verl", "Verl",
            wikimedia_icon_urls("commons/c/ce/SC_Verl_Logo.svg")
        ),
        "SVM": (
            "SV Meppen", "SV Meppen", "Meppen",
            wikimedia_icon_urls("commons/4/45/Logo_SV_Meppen_2019.svg")
        ),
        "MAN": (
            "SV Waldhof Mannheim", "SV Waldhof Mannheim", "Mannheim",
            wikimedia_icon_urls("commons/1/1c/SV_Waldhof_Mannheim_Wappen.svg")
        ),
        "WIE": (
            "SV Wehen Wiesbaden", "SV Wehen Wiesbaden", "Wiesbaden",
            wikimedia_icon_urls("de/3/3d/Logo_SV_Wehen_Wiesbaden.svg")
        ),
        "MÜN": (
            "TSV 1860 München", "TSV 1860 München", "1860 München",
            wikimedia_icon_urls("commons/4/48/TSV_1860_M%C3%BCnchen.svg")
        ),
        "HAV": (
            "TSV Havelse", "TSV Havelse", "Havelse",
            wikimedia_icon_urls("commons/8/89/TSV_Havelse_logo.svg")
        ),
        "TÜR": (
            "Türkgücü München", "Türkgücü München", "Türkgücü",
            wikimedia_icon_urls("commons/f/fe/T%C3%BCrkg%C3%BCc%C3%BC_"
                                "M%C3%BCnchen_Logo.svg")
        ),
        "OSN": (
            "VfL Osnabrück", "VfL Osnabrück", "Osnabrück",
            wikimedia_icon_urls(
                "commons/5/59/Logo_VfL_Osnabrueck_since_2017.svg")
        ),
        "WÜR": (
            "Würzburger Kickers", "Würzburger Kickers", "Würzburg",
            wikimedia_icon_urls(
                "commons/0/0c/W%C3%BCrzburger_Kickers_Logo.svg")
        ),
        "BV2": (
            "Borussia Dortmund II", "Borussia Dortmund II", "Dortmund II",
            wikimedia_icon_urls("commons/6/67/Borussia_Dortmund_logo.svg")
        ),
        "ZWI": (
            "FSV Zwickau", "FSV Zwickau", "Zwickau",
            wikimedia_icon_urls("de/0/01/FSV_Zwickau_Logo.svg")
        )
    }
    openligadb_map = {
        info[0]: (
            info[1],
            info[2],
            abbreviation,
            info[3]
        )
        for abbreviation, info in team_map.items()
    }
    return openligadb_map[team_name]


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
