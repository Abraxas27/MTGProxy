# coding : utf-8
import os
import re
import shutil
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote_plus
import param
from log import logger as log


INPUT_REGEX = "^(?:SB\s?\:*\s?)?(\d+)\s+(?:\[(.{2}.?)\])?\s?([\w,'\-\s\(\)\./]*?)(?:\s*#+.*)?$"
ONLINE_REGEX = "(http://magiccards\.info/scans/en/\w{2,3}/\d{1,3}\w?\.jpg)"
LAND_VERSION_REGEX = '\s?\(v\.?\s?([0-9]*)\)'

LAND_NAMES = ['plains', 'island', 'swamp', 'mountain', 'forest']

current_proxy_id = 1


def copy_card(path, quantity):
    global current_proxy_id
    for i in range(0, int(quantity)):
        shutil.copy(path, os.path.join(param.OUTPUT_PROXY_DIR, str(current_proxy_id) + ".jpg"))
        current_proxy_id += 1


def adapt_regex_if_land(regex, card_name):
    reg = re.compile(LAND_VERSION_REGEX, re.IGNORECASE)
    if reg.search(card_name):
        land_version = reg.findall(card_name)[0]
        name = reg.sub('', card_name)
        regex = re.escape(name) + '\s?\(v\.\s?' + land_version + '\)'
    elif card_name in LAND_NAMES:  # TODO: make land card variation optional
        regex += '\s?\(v\.\s?1\)'
    return regex


def find_card_offline(name, cardset=None):
    regex = name.lower()
    regex = adapt_regex_if_land(regex, name) + '(?! )\.'  # not followed by a space, but followed by a dot
    for edition_trigram in param.EDITION_TRIGRAMS:
        try:
            edition_scan_path = os.path.join(param.SCANS_DIR, edition_trigram)
            reg = re.compile(regex, re.IGNORECASE)
            for filename in os.listdir(edition_scan_path):
                if reg.match(filename):
                    edition_file_path = os.path.join(edition_scan_path, filename)
                    if os.path.getsize(edition_file_path) > 0:
                        found = edition_file_path
                        if not cardset or os.path.basename(edition_scan_path) == cardset:
                            return found
        except IOError:
            continue


def is_double_faced_card(cardname):
    return True if cardname.lower() in param.CARDS_DOUBLE_FACED.keys() else False


def create_proxy_offline(quantity, cardname, cardset=''):
    cardname_splitted = cardname.split('//')[0].rstrip().lower()
    if is_double_faced_card(cardname_splitted):
        if not create_proxy_offline(quantity, param.CARDS_DOUBLE_FACED[cardname_splitted], cardset):
            log.error("'{}' not found in scans directory ".format(cardname_splitted))
            return_code = 0
        else:
            filepath = find_card_offline(cardname_splitted, cardset)
            copy_card(filepath, quantity)
            log.info("{} '{}' created using file {}".format(quantity, cardname_splitted, filepath))
            return_code = 1
    else:
        cardname_replaced = re.sub("\s*/{1,2}\s*", "_", cardname)
        filepath = find_card_offline(cardname_replaced, cardset)
        if filepath:
            copy_card(filepath, quantity)
            log.info("{} '{}' created using file {}".format(quantity, cardname_replaced, filepath))
            return_code = 1
        else:
            log.error("'{}' not found in scans directory ".format(cardname_replaced))
            return_code = 0
    return return_code


def create_proxy_online(quantity, cardname, cardset=''):
    global current_proxy_id
    if cardset == '':
        searchurl = "http://magiccards.info/query?q=!{}&v=card&s=cname".format(
            quote_plus(cardname.lower()))
    else:
        searchurl = "http://magiccards.info/query?q={}+e%3A{}&v=card&s=cname".format(
            quote_plus(cardname.lower()),
            quote_plus(cardset.lower()))
    with urlopen(searchurl) as response:
        httpcontent = response.readlines()
    if re.search(ONLINE_REGEX, str(httpcontent)):
        imageurl = re.findall(ONLINE_REGEX, str(httpcontent))[0]
        tmpfile = urlretrieve(imageurl)[0]
        copy_card(tmpfile, quantity)
        log.info("{} '{}' created using {}".format(quantity, cardname, imageurl))
        return 1
    else:
        log.error("'" + cardname + "' not found online with URL " + searchurl)
        return 0


def card_not_found(name):
    with open(param.NOT_FOUND_FILE, 'a') as fd:
        fd.write(name)


def process_input_file(input_file):
    with open(input_file, 'r', encoding='utf8') as fd:
        lines = fd.readlines()
    compiled_regex = re.compile(INPUT_REGEX, re.M | re.I)
    for line in lines:
        if compiled_regex.match(line) is not None:
            quantity, cardset, cardname = map(lambda x: x.strip(), compiled_regex.findall(line)[0])
            log.debug("quantity : " + cardname)
            log.debug("quantity : " + quantity)
            log.debug("cardset : " + cardset)
            if not cardset:
                log.info("Searching for '{}' in the most recent edition".format(cardname))
            else:
                log.info("Searching for '{}' in [{}] edition".format(cardname, cardset))
            if param.MODE_PRIORITY.lower() == 'offline':
                if not create_proxy_offline(quantity, cardname, cardset):
                    if param.TRY_OTHER_METHOD and not create_proxy_online(quantity, cardname, cardset):
                            card_not_found(line)
                    else:
                        card_not_found(line)
            else:
                if not create_proxy_online(quantity, cardname, cardset):
                    if param.TRY_OTHER_METHOD and not create_proxy_offline(quantity, cardname, cardset):
                        card_not_found(line)
                    else:
                        card_not_found(line)


def delete_older_work():
    os.makedirs(param.OUTPUT_DIR, exist_ok=True)
    for root, dirs, files in os.walk(param.OUTPUT_DIR, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.makedirs(param.OUTPUT_PROXY_DIR)
    log.debug(os.path.join(param.OUTPUT_DIR, param.OUTPUT_FILE_NAME))
    if param.OUTPUT_FILE_EXTENSION == '.sla':
        sla_filename = os.path.join(param.CONF_DIR, "Proxy.sla")
        shutil.copy(sla_filename, os.path.join(param.OUTPUT_DIR, param.OUTPUT_FILE_NAME))
    open(param.NOT_FOUND_FILE, 'w').close()


if __name__ == '__main__':
    delete_older_work()
    process_input_file(param.PROXY_FILE)
    if param.OUTPUT_TYPE == 'pdf':
        import pdf
        pdf.print_pdf(current_proxy_id - 1, os.path.join(param.OUTPUT_DIR, param.OUTPUT_FILE_NAME))
