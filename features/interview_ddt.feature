Feature: Interview library (data driven)

  @smoke
  Scenario Outline: The search box keeps the query <query>
    Given the "Interview Prep" page is open
    When the user searches the interview library for "<query>"
    Then the search box contains "<query>"

    Examples:
      | query      |
      | Playwright |
      | Selenium   |
      | Cypress    |
      | API        |

  # filter is the end of the checkbox id on the site: tech-<filter>.
  # count is the number in brackets next to the checkbox label.
  @smoke
  Scenario Outline: The <topic> checkbox filters questions
    Given the "Interview Prep" page is open
    When the user ticks the topic filter "<filter>"
    Then the topic filter "<filter>" is selected
    And the result count reads "<count> questions"
    And every visible question mentions "<topic>"

    Examples:
      | topic      | filter     | count |
      | JavaScript | javascript | 21    |
      | Java       | java       | 53    |
      | Python     | python     | 20    |
      | Selenium   | selenium   | 36    |
      | Playwright | playwright | 22    |
      | Cypress    | cypress    | 19    |
      | SQL        | sql        | 20    |
