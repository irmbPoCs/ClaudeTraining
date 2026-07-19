# Tool Use

## How Tool Use Works

Tool use follows a specific back-and-forth pattern between your application and Claude. Here's the complete flow:

![alt text](image.png)

## Weather Example in Practice

Let's see how this works with the weather question. The process becomes much more specific:

![alt text](image-1.png)

## What Are Tool Functions?

A tool function is a plain Python function that gets executed automatically when Claude decides it needs extra information to help a user. For example, if someone asks "What time is it?", Claude would call your date/time tool to get the current time.

![alt text](image-2.png)

## Best Practices for Tool Functions

When writing tool functions, follow these guidelines:

* Use descriptive names: Both your function name and parameter names should clearly indicate their purpose
* Validate inputs: Check that required parameters aren't empty or invalid, and raise errors when they are
* Provide meaningful error messages: Claude can see error messages and might retry the function call with corrected parameters

The validation is particularly important because Claude learns from errors. If you raise a clear error like "Location cannot be empty", Claude might try calling the function again with a proper location value.