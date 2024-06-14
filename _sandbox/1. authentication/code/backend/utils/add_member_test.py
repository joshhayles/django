import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

mailchimp = MailchimpMarketing.Client()
mailchimp.set_config({
  "api_key": "removed",
  "server": "us10"
})

list_id = "removed"

member_info = {
    "email_address": "theJoshua32@gmail.com",
    "status": "subscribed",
    "merge_fields": {
      "FNAME": "Joshua",
      "LNAME": "H.",
      "MMERGE3": {
        "addr1": "8720 palomino ridge",
        "city": "Peyton",
        "state": "CO",
        "zip": "80831",
      }
    }
  }

try:
  response = mailchimp.lists.add_list_member(list_id, member_info)
  print("response: {}".format(response))
except ApiClientError as error:
  print("An exception occurred: {}".format(error.text))