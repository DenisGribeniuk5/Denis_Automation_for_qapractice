# Data-driven version of contact.feature.
# Each row in Examples fills the form once, with one topic from the dropdown.
# The scenario does not click "Open email draft", because that opens the mail app.
Feature: Contact form (data driven)

  @smoke
  Scenario Outline: The form accepts a message about <topic>
    Given the "Contact" page is open
    When the user fills the contact form with "<name>", "<email>", "<topic>" and "<message>"
    Then the contact form shows "<name>", "<email>", "<topic>" and "<message>"
    And the send button is visible

    Examples:
      | name          | email                     | topic                           | message                                     |
      | Anna Smith    | anna.smith@example.com    | General question                | Practice message. Do not send. Hello.       |
      | Ben Lee       | ben.lee@example.com       | Report a bug on a practice page | Practice message. Do not send. Bug found.   |
      | Chloe Martin  | chloe.martin@example.com  | Suggest a topic or feature      | Practice message. Do not send. New idea.    |
      | David O'Brien | david.obrien@example.com  | Content or copyright query      | Practice message. Do not send. Copyright.   |
      | Eva Novak     | eva.novak@example.com     | Privacy request                 | Practice message. Do not send. Delete data. |
