import logging
from time import sleep
from xml.etree.ElementTree import Element, SubElement, ElementTree

from pymysql import connect
from schedule import Scheduler

import settings


logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename=settings.LOG_PATH)


def run():
    logging.info('Service run.')
    phones = _get_phones_from_database(settings.DATABASE)
    if phones:
        logging.info('Get data success.')
        generate_files(phones)


def _get_phones_from_database(database):
    phones = []
    try:
        connection = connect(**database)
        phones = _get_phones_from_connection(connection)
    except:
        logging.error('Error getting connection to database.')
    return phones


def _get_phones_from_connection(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT extension, name FROM users')
        return [row for row in cursor]
    except:
        logging.error('An error occurred while retrieving data from the database.')


def generate_files(phones):
    if hasattr(settings, 'XML_PATH'):
        generate_phonebook_xml(phones)


def generate_phonebook_xml(phones):
    try:
        xml = _create_xml_phonebook(phones)
    except:
        logging.error('Error creating xml file.')
    try:
        tree = ElementTree(xml)
        tree.write(settings.XML_PATH)
        logging.info('The XML file is written in {}'.format(settings.XML_PATH))
    except:
        logging.error('Error while writing xml file.')


def _create_xml_phonebook(phones):
    address_book_element = Element('AddressBook')
    for phone in phones:
        contact_element = SubElement(address_book_element, 'Contact')

        first_name_element = SubElement(contact_element, 'LastName')
        first_name_element.text = phone['name']

        phone_element = SubElement(contact_element, 'Phone')
        phone_number_element = SubElement(phone_element, 'phonenumber')
        phone_number_element.text = phone['extension']
        account_index_element = SubElement(phone_element, 'accountindex')
        account_index_element.text = phone['extension']

        group = str(phone['extension'])[:2]

        groups_element = SubElement(contact_element, 'Groups')
        group_uid_element = SubElement(groups_element, 'groupid')
        group_uid_element.text = group
    return address_book_element


def _get_schedule_from_settings(settings):
    schedule = Scheduler()

    if hasattr(settings, 'UPDATE_TIME_HOUR') and settings.UPDATE_TIME_HOUR:
        schedule.every(settings.UPDATE_TIME_HOUR)\
                .hours.do(run)
    if hasattr(settings, 'UPDATE_TIME_MIN') and settings.UPDATE_TIME_MIN:
        schedule.every(settings.UPDATE_TIME_MIN)\
                .minutes.do(run)
    if hasattr(settings, 'UPDATE_TIME_SEC') and settings.UPDATE_TIME_SEC:
        schedule.every(settings.UPDATE_TIME_SEC)\
                .seconds.do(run)

    return schedule


if __name__ == '__main__':
    schedule = _get_schedule_from_settings(settings)
    logging.info('Service up with {}'.format(schedule.jobs))
    while True:
        schedule.run_pending()
        sleep(1)
