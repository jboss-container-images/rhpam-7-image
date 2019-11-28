@rhpam-7/rhpam77-smartrouter
Feature: RHPAM Smart Router tests

   Scenario: Test REST API is available and valid
     When container is ready
     Then check that page is served
         | property | value |
         | port     | 9000  |
         | path     | / |
         | expected_phrase | SUCCESS |
