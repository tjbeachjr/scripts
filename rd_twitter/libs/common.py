# -*- coding: latin-1 -*-
"""
*******************************************************************************
** Script Name: common.py
** Author(s):   Terrence Beach (tjbeachjr@gmail.com)
*******************************************************************************

** Description:

Common functions used by the other libraries / scripts

*******************************************************************************
"""
import logging
import smtplib

"""
setup_logger

Setup the logger object
"""

def setup_logger(log_name):
    log = logging.getLogger(log_name)
    log.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s\t%(asctime)s\t%(name)s\t%(message)s")
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log


"""
send_email

Use the Python smtplib to send an email
"""

def send_email(server_addr, from_addr, to_addrs, subject, body):
    message = "From: %s\r\nTo: %s\r\nSubject: %s\r\n%s" % (from_addr, ",".join(to_addrs), subject, body)
    server = smtplib.SMTP(server_addr)
    server.sendmail(from_addr, to_addrs, message)
    server.quit()

        
country_codes = {
    "AD": "ANDORRA",
    "AE": "UAE",
    "AF": "AFGHANISTAN",
    "AG": "ANTIGUAANDBARBUDA",
    "AI": "ANGUILLA",
    "AL": "ALBANIA",
    "AM": "ARMENIA",
    "AN": "NETHERLANDSANTILLES",
    "AO": "ANGOLA",
    "AQ": "ANTARCTICA",
    "AR": "ARGENTINA",
    "AS": "AMERICANSAMOA",
    "AT": "AUSTRIA",
    "AU": "AUSTRALIA",
    "AW": "ARUBA",
    "AZ": "AZERBAIJAN",
    "BA": "BOSNIAANDHERZEGOVINA",
    "BB": "BARBADOS",
    "BD": "BANGLADESH",
    "BE": "BELGIUM",
    "BF": "BURKINAFASO",
    "BG": "BULGARIA",
    "BH": "BAHRAIN",
    "BI": "BURUNDI",
    "BJ": "BENIN",
    "BM": "BERMUDA",
    "BN": "BRUNEIDARUSSALAM",
    "BO": "BOLIVIA",
    "BR": "BRAZIL",
    "BS": "BAHAMAS",
    "BT": "BHUTAN",
    "BV": "BOUVETISLAND",
    "BW": "BOTSWANA",
    "BY": "BELARUS",
    "BZ": "BELIZE",
    "CA": "CANADA",
    "CC": "COCOSISLANDS",
    "CF": "CENTRALAFRICANREPUBLIC",
    "CG": "CONGO",
    "CH": "SWITZERLAND",
    "CI": "IVORYCOAST",
    "CK": "COOKISLANDS",
    "CL": "CHILE",
    "CM": "CAMEROON",
    "CN": "CHINA",
    "CO": "COLOMBIA",
    "CR": "COSTARICA",
    "CS": "CZECHOSLOVAKIA",
    "CU": "CUBA",
    "CV": "CAPEVERDE",
    "CX": "CHRISTMASISLAND",
    "CY": "CYPRUS",
    "CZ": "CZECHREPUBLIC",
    "DE": "GERMANY",
    "DJ": "DJIBOUTI",
    "DK": "DENMARK",
    "DM": "DOMINICA",
    "DO": "DOMINICANREPUBLIC",
    "DZ": "ALGERIA",
    "EC": "ECUADOR",
    "EE": "ESTONIA",
    "EG": "EGYPT",
    "EH": "WESTERNSAHARA",
    "ER": "ERITREA",
    "ES": "SPAIN",
    "ET": "ETHIOPIA",
    "FI": "FINLAND",
    "FJ": "FIJI",
    "FK": "FALKLANDISLANDS",
    "FM": "MICRONESIA",
    "FO": "FAROEISLANDS",
    "FR": "FRANCE",
    "FX": "FRANCE",
    "GA": "GABON",
    "GB": "UK",
    "GD": "GRENADA",
    "GE": "GEORGIA",
    "GF": "FRENCHGUIANA",
    "GH": "GHANA",
    "GI": "GIBRALTAR",
    "GL": "GREENLAND",
    "GM": "GAMBIA",
    "GN": "GUINEA",
    "GP": "GUADELOUPE",
    "GQ": "EQUATORIALGUINEA",
    "GR": "GREECE",
    "GS": "SOUTHGEORGIA",
    "GT": "GUATEMALA",
    "GU": "GUAM",
    "GW": "GUINEA-BISSAU",
    "GY": "GUYANA",
    "HK": "HONGKONG",
    "HM": "HEARDANDMCDONALDISLANDS",
    "HN": "HONDURAS",
    "HR": "CROATIA",
    "HT": "HAITI",
    "HU": "HUNGARY",
    "ID": "INDONESIA",
    "IE": "IRELAND",
    "IL": "ISRAEL",
    "IN": "INDIA",
    "IO": "BRITISHINDIANOCEANTERRITORY",
    "IQ": "IRAQ",
    "IR": "IRAN",
    "IS": "ICELAND",
    "IT": "ITALY",
    "JM": "JAMAICA",
    "JO": "JORDAN",
    "JP": "JAPAN",
    "KE": "KENYA",
    "KG": "KYRGYZSTAN",
    "KH": "CAMBODIA",
    "KI": "KIRIBATI",
    "KM": "COMOROS",
    "KN": "SAINTKITTSANDNEVIS",
    "KP": "NORTHKOREA",
    "KR": "SOUTHKOREA",
    "KW": "KUWAIT",
    "KY": "CAYMANISLANDS",
    "KZ": "KAZAKHSTAN",
    "LA": "LAOS",
    "LB": "LEBANON",
    "LC": "SAINTLUCIA",
    "LI": "LIECHTENSTEIN",
    "LK": "SRILANKA",
    "LR": "LIBERIA",
    "LS": "LESOTHO",
    "LT": "LITHUANIA",
    "LU": "LUXEMBOURG",
    "LV": "LATVIA",
    "LY": "LIBYA",
    "MA": "MOROCCO",
    "MC": "MONACO",
    "MD": "MOLDOVA",
    "MG": "MADAGASCAR",
    "MH": "MARSHALLISLANDS",
    "MK": "MACEDONIA",
    "ML": "MALI",
    "MM": "MYANMAR",
    "MN": "MONGOLIA",
    "MO": "MACAU",
    "MP": "NORTHERNMARIANAISLANDS",
    "MQ": "MARTINIQUE",
    "MR": "MAURITANIA",
    "MS": "MONTSERRAT",
    "MT": "MALTA",
    "MU": "MAURITIUS",
    "MV": "MALDIVES",
    "MW": "MALAWI",
    "MX": "MEXICO",
    "MY": "MALAYSIA",
    "MZ": "MOZAMBIQUE",
    "NA": "NAMIBIA",
    "NC": "NEWCALEDONIA",
    "NE": "NIGER",
    "NF": "NORFOLK",
    "NG": "NIGERIA",
    "NI": "NICARAGUA",
    "NL": "NETHERLANDS",
    "NO": "NORWAY",
    "NP": "NEPAL",
    "NR": "NAURU",
    "NT": "NEUTRALZONE",
    "NU": "NIUE",
    "NZ": "NEWZEALAND",
    "OM": "OMAN",
    "PA": "PANAMA",
    "PE": "PERU",
    "PF": "FRENCHPOLYNESIA",
    "PG": "PAPUANEWGUINEA",
    "PH": "PHILIPPINES",
    "PK": "PAKISTAN",
    "PL": "POLAND",
    "PM": "STPIERREANDMIQUELON",
    "PN": "PITCAIRN",
    "PR": "PUERTORICO",
    "PT": "PORTUGAL",
    "PW": "PALAU",
    "PY": "PARAGUAY",
    "QA": "QATAR",
    "RE": "REUNION",
    "RO": "ROMANIA",
    "RU": "RUSSIA",
    "RW": "RWANDA",
    "SA": "SAUDIARABIA",
    "SB": "SOLOMONISLANDS",
    "SC": "SEYCHELLES",
    "SD": "SUDAN",
    "SE": "SWEDEN",
    "SG": "SINGAPORE",
    "SH": "STHELENA",
    "SI": "SLOVENIA",
    "SJ": "SVALBARDANDJANMAYENISLANDS",
    "SK": "SLOVAKREPUBLIC",
    "SL": "SIERRALEONE",
    "SM": "SANMARINO",
    "SN": "SENEGAL",
    "SO": "SOMALIA",
    "SR": "SURINAME",
    "ST": "SAOTOMEANDPRINCIPE",
    "SU": "USSR",
    "SV": "ELSALVADOR",
    "SY": "SYRIA",
    "SZ": "SWAZILAND",
    "TC": "TURKSANDCAICOS",
    "TD": "CHAD",
    "TF": "FRENCHSOUTHERNTERRITORIES",
    "TG": "TOGO",
    "TH": "THAILAND",
    "TJ": "TAJIKISTAN",
    "TK": "TOKELAU",
    "TM": "TURKMENISTAN",
    "TN": "TUNISIA",
    "TO": "TONGA",
    "TP": "EASTTIMOR",
    "TR": "TURKEY",
    "TT": "TRINIDADANDTOBAGO",
    "TV": "TUVALU",
    "TW": "TAIWAN",
    "TZ": "TANZANIA",
    "UA": "UKRAINE",
    "UG": "UGANDA",
    "UK": "UK",
    "UM": "USMINOROUTLYINGISLANDS",
    "US": "USA",
    "UY": "URUGUAY",
    "UZ": "UZBEKISTAN",
    "VA": "VATICANCITY",
    "VC": "SAINTVINCENTANDTHEGRENADINES",
    "VE": "VENEZUELA",
    "VG": "VIRGINISLANDS",
    "VI": "VIRGINISLANDS",
    "VN": "VIETNAM",
    "VU": "VANUATU",
    "WF": "WALLISANDFUTUNA",
    "WS": "SAMOA",
    "YE": "YEMEN",
    "YT": "MAYOTTE",
    "YU": "YUGOSLAVIA",
    "ZA": "SOUTHAFRICA",
    "ZM": "ZAMBIA",
    "ZR": "ZAIRE",
    "ZW": "ZIMBABWE",
    "COM": "USA",
    "EDU": "USA",
    "GOV": "USA",
    "INT": "INTERNATIONAL",
    "MIL": "USA",
    "NET": "USA",
    "ORG": "USA",
    "ARPA": "USA"}