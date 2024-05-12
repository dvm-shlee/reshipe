## **YAML Recipe and Parsing Guide: Comprehensive Example**

### **Overview**
This guide illustrates a sophisticated usage of a YAML recipe to unify and transform detailed customer information from multiple Python objects into a structured format. The recipe enhances data integration by incorporating additional fields, applying conditional logic, and executing scripts.

### **Example Data**
Consider a Customer instance structured as follows:

**Python Objects:**
```python
Customer:
    profile = {
        "customer_id": "C001",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "orders": [123, 456, 789],
        "loyalty_points": 1200
    }
    details = {
        "customer_id": "C001",
        "address": "123 Elm Street",
        "phone": "555-1234",
        "preferred_contact": ["email", "phone"]
    }
```

### **YAML Recipe**
This recipe is designed to extract and process diverse customer information, from basic contact details to specific preferences and rewards calculations.

**YAML Recipe:**
```yaml
package: xnippet>=0.1.0
plugin: plugin_example
recipe:
  name: customer_info_aggregator
  version: 1.0

classifier:
  customer_info:
    customer_name: profile.name
    email_address: profile.email
    second_order:
      key: profile.orders
      idx: 1
    address: details.address
    phone_number: details.phone
    preferred_contact_method:
      key: details.preferred_contact
      where: email  # Assumes functionality to prioritize 'email' over other contacts
    reward_points:
      setup-script: "ratio = 10"
      loyalty_points: profile.loyalty_points
      script: "loyalty_points / ratio"  # Converts loyalty points into reward points
```

### **Parsed Output**
```json
{
  "customer_info": {
    "customer_name": "John Doe",
    "email_address": "johndoe@example.com",
    "second_order": 456,
    "address": "123 Elm Street",
    "phone_number": "555-1234",
    "preferred_contact_method": "email",
    "reward_points": 120  # Assuming 1200 loyalty points
  }
}
```

### **Explanation**
- **`customer_name`** and **`email_address`**: Extracted directly from the customer's profile.
- **`second_order`**: Retrieves the second item from the orders list in the profile.
- **`address`** and **`phone_number`**: Mapped directly from the customer's details.
- **`preferred_contact_method`**: Demonstrates conditional selection, favoring 'email' as the primary contact method based on the specified conditions.
- **`reward_points`**: Implements a script to calculate reward points from loyalty points, illustrating the recipe's capability to perform arithmetic operations directly.
