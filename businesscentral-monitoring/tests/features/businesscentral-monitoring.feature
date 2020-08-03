@rhpam-7/rhpam-businesscentral-monitoring-rhel8
Feature: Standalone Business Central Monitoring tests

  Scenario: Web console is available
    When container is ready
    Then check that page is served
         | property | value |
         | port     | 8080  |
         | path     | /kie-wb.jsp |
         | expected_status_code | 200 |
         | wait     | 120   |
