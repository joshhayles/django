import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from environs import Env 

env = Env()
env.read_env()

def add_member_to_mailchimp(email, first_name, last_name, address):
    mailchimp = MailchimpMarketing.Client()
    mailchimp.set_config({
        "api_key": env.str("MAILCHIMP_API_KEY"),
        "server": "us10"
    })

    list_id = env.str("MAILCHIMP_LIST_ID")

    member_info = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": {
            "FNAME": first_name,
            "LNAME": last_name,
            "MMERGE3": {
                "addr1": address.get("addr1", ""),
                "city": address.get("city", ""),
                "state": address.get("state", ""),
                "zip": address.get("zip", ""),
            }
        }
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("Mailchimp response: {}".format(response))
    except ApiClientError as error:
        print("Mailchimp error: {}".format(error.text))