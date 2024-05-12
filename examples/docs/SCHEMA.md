## **YAML Data Schema Document Guide**

### **Overview**
This guide details the YAML Data Schema for validating data fields within a software application or plugin. The specification ensures each data field meets the required standards for data type, format, and allowable values. This document is used primarily in environments where data integrity and compliance are critical.

### **Specification Document Structure**

#### **Basic Elements**
- **Package**: Specifies the software package that the specification is intended for.
- **Plugin**: Indicates the specific plugin the specification applies to.
- **Spec**: Outlines the metadata about the specification, including its name and version.

#### **Fields Definition**
Each field in the dataset is described in detail, specifying the validation requirements and whether the field is optional.

**Example Schema YAML Document:**
```yaml
package: xnippet>=0.1.0
plugin: plugin_example
schema:
  name: schema_snippet
  version: 0.0.1

  fields:
    name:
      description: "Name of person"
      validation:
        type: string
        pattern: "^[a-zA-Z]+ [a-zA-Z]+$"
        pattern_description: "FirstName LastName"
      optional: false

    favorite_fruit:
      description: "Favorite fruit among apple, banana, orange, pineapple"
      validation:
        type: string
        allowed_values:
        - apple
        - banana
        - orange
        - pineapple
      optional: true

    email:
      description: "Email address of the person"
      validation:
        type: string
        pattern: "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        pattern_description: "Valid email format"
      optional: false

    age:
      description: "Age of the person, must be an integer between 18 and 99"
      validation:
        type: integer
        range:
          min: 18
          max: 99
      optional: false

    date_of_birth:
      description: "Date of birth in YYYY-MM-DD format"
      validation:
        type: date
        pattern: "^\d{4}-\d{2}-\d{2}$"
        pattern_description: "YYYY-MM-DD"
      optional: true

    newsletter_subscribed:
      description: "Whether the person is subscribed to the newsletter"
      validation:
        type: boolean
        allowed_values:
        - true
        - false
      optional: true

    hobbies:
      description: "List of hobbies, up to 5, as strings"
      validation:
        type: array
        item_type: string
        min_items: 1
        max_items: 5
      optional: true
```

### **Explanation of Fields**
- **`type`**: Specifies the data type (e.g., string, integer, date, boolean).
- **`pattern`**: For string types, a regex pattern may be specified to validate the format.
- **`allowed_values`**: Defines a list of permissible values.
- **`range`**: For numerical types, specifies the minimum and maximum allowable values.
- **`item_type`**, **`min_items`** and **`max_items`**: For array, defines the type of items in the array and the minimum or maximum number or both allowed.
- **`optional`**: Indicates whether the field is mandatory or optional.

### **Usage**
This data schema is integrated into the software to validate incoming data, ensuring that all entries conform to the defined standards before being processed or stored. This approach enhances data integrity and reduces errors due to incorrect data formats or values.

--- 

This guideline will help users and developers understand how to define and use the YAML specifications for data validation within your software environment.
