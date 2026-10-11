# Every card link says "Start practising", so the path is what tells them apart.
# The store path really is spelled "ecommerece" on the site.
Feature: Practice sites (data driven)

  @smoke
  Scenario Outline: The <sandbox> sandbox opens from its card
    Given the "Practice Sites" page is open
    Then the sandbox link to "<path>" is visible
    When the user opens the sandbox link to "<path>"
    Then the address ends with "<path>"

    Examples:
      | sandbox         | path                            |
      | Login           | /practice-login-form            |
      | Web form        | /practice-forms                 |
      | Store           | /practice-ecommerece-website    |
      | Flight booking  | /flight-booking-scenarios       |
      | UI elements     | /practice-different-ui-elements |
      | XPath guide     | /SeleniumXPathGuide             |
      | Forgot password | /forget-password                |
      | Register        | /register                       |
      | API playground  | /api-playground                 |
