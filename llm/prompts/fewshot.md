# Scam Detection - Few-Shot Learning

You are an expert at identifying scams in text messages. Learn from these examples and apply the same reasoning to new messages.

## Example 1:
**Message:** "Congratulations! You've won a free iPhone. Click this link and enter your bank details to claim."

**Analysis:**
```json
{
  "label": "Scam",
  "reasoning": "This message uses classic scam tactics: unexpected reward, request for sensitive financial information, and urgency through a link click requirement.",
  "intent": "Trick user into sharing banking information",
  "risk_factors": ["Unexpected reward", "Link click", "Bank details request"]
}
```

## Example 2:
**Message:** "Dear customer, your bill is due. Please visit our portal and pay by 5th."

**Analysis:**
```json
{
  "label": "Not Scam",
  "reasoning": "This is a standard billing reminder with no threatening or suspicious tone. No request for sensitive info outside normal billing process.",
  "intent": "Inform about billing and prompt payment",
  "risk_factors": []
}
```

## Example 3:
**Message:** "URGENT: Your account will be suspended! Call 555-FAKE immediately or lose access forever!"

**Analysis:**
```json
{
  "label": "Scam",
  "reasoning": "Uses high urgency, threatens account suspension, and provides suspicious phone number. Legitimate companies rarely use such aggressive tactics.",
  "intent": "Create panic to force immediate action",
  "risk_factors": ["High urgency", "Threats", "Suspicious phone number", "Fear tactics"]
}
```

## Example 4:
**Message:** "Hello, this is a reminder from UtilityCo: your payment of $75 is due on July 10. Visit our secure portal to pay or call our support line if you have questions."

**Analysis:**
```json
{
  "label": "Not Scam",
  "reasoning": "Clear sender identification, reasonable request related to a known service, no unusual urgency or request for sensitive info beyond normal payment.",
  "intent": "Notify customer about an upcoming payment",
  "risk_factors": []
}
```

## Example 5:
**Message:** "Your subscription will renew next week. No action needed unless you'd like to cancel. Check your account settings for details."

**Analysis:**
```json
{
  "label": "Not Scam",
  "reasoning": "Informational tone, explains next steps and provides a benign option to cancel; no threats, links, or demands for sensitive data.",
  "intent": "Inform about upcoming renewal",
  "risk_factors": []
}
```

## Example 6:
**Message:** "Congratulations! You've been selected for a $5,000 grant. Click here and enter your social security number to claim." 

**Analysis:**
```json
{
  "label": "Scam",
  "reasoning": "Unexpected large reward combined with a request for highly sensitive information (SSN) and a click-through instruction are classic scam indicators.",
  "intent": "Obtain sensitive personal information for fraudulent use",
  "risk_factors": ["Unexpected reward", "Request for SSN", "Link click"]
}
```

## Example 7:
**Message:** "Act now! You've won a holiday voucher. Provide your card details to pay a small processing fee or the prize will be forfeited." 

**Analysis:**
```json
{
  "label": "Scam",
  "reasoning": "Pressure to pay a fee for a prize and a request for card details are common advance-fee scam tactics; legitimate prizes don't require payment.",
  "intent": "Extract payment/card details",
  "risk_factors": ["Advance fee request", "Payment for prize", "Card details request", "High pressure"]
}
```

## Example 8:
**Message:** "We noticed unusual activity on your bank account. If this was you, ignore. If not, reply with 'NO' or call this number." 

**Analysis:**
```json
{
  "label": "Uncertain",
  "reasoning": "Claims unusual activity which could be legitimate fraud alert, but requests a reply or call without clear verified sender or secure instructions, making it suspicious.",
  "intent": "Potentially verify account activity or phish for response",
  "risk_factors": ["Unclear sender", "Action requested via reply/call", "Potential social engineering"]
}
```

## Example 9:
**Message:** "Free tax help available today. Reply with your income range to see if you qualify." 

**Analysis:**
```json
{
  "label": "Uncertain",
  "reasoning": "Could be a benign outreach for services, but asking for income range via message is sensitive and could be used for profiling or fraud if not from a verified source.",
  "intent": "Assess eligibility for a service",
  "risk_factors": ["Request for sensitive financial info", "Unverified sender"]
}
```

## Example 10:
**Message:** "Your delivery is arriving today. If you won't be home, reply 'HOLD' with a safe address for redelivery." 

**Analysis:**
```json
{
  "label": "Uncertain",
  "reasoning": "Typical shipping notice but asking for an alternate address via reply can be legitimate; however it could be abused to redirect packages if sender isn't verified.",
  "intent": "Arrange delivery preferences",
  "risk_factors": ["Request to provide alternative address", "Potential package redirect risk"]
}
```

## Example 11:
**Message:** "This is the CEO. I am in a meeting and need you to buy $500 in gift cards right now. Send me the codes and keep this confidential."

**Analysis:**
```json
{
  "label": "Scam",
  "reasoning": "The sender creates urgency, requests an irreversible payment through gift cards, and demands secrecy. These are strong impersonation and payment-fraud indicators.",
  "intent": "Impersonate an executive to steal gift card value",
  "risk_factors": ["Urgent payment request", "Gift cards", "Secrecy demand", "Unverified executive identity"]
}
```

## Example 12:
**Message:** "Your library hold is ready for pickup. Please collect it by Friday. You can check your account by opening the library's official website or visiting the branch."

**Analysis:**
```json
{
  "label": "Not Scam",
  "reasoning": "This is a routine service reminder with a relevant action and safe ways to check details. It does not request payment, credentials, or sensitive information.",
  "intent": "Notify a library patron that a reserved item is available",
  "risk_factors": []
}
```

## Example 13:
**Message:** "Congratulations, you got the remote job! We will mail you a check for equipment. Deposit it today, buy from our approved vendor, and send back any leftover funds."

**Analysis:**
```json
{
  "label": "Scam",
  "reasoning": "The message asks a new hire to deposit a check, spend the funds through a specified vendor, and return the remainder. This is a common fake-check scheme; the deposit may later be reversed after the money is sent.",
  "intent": "Use a fake check to get the recipient to send money",
  "risk_factors": ["Unsolicited check", "Urgent deposit request", "Specified vendor", "Request to return leftover funds"]
}
```

## Example 14:
**Message:** "Reminder: your dental cleaning is Tuesday at 10:00 a.m. To reschedule, call the clinic using the number on your appointment card."

**Analysis:**
```json
{
  "label": "Not Scam",
  "reasoning": "This is a straightforward appointment reminder. It directs the recipient to contact the clinic using contact details they already have and does not request payment or personal information by message.",
  "intent": "Remind a patient of an upcoming appointment",
  "risk_factors": []
}
```

## Example 15:
**Message:** "Your bank flagged a card purchase. If you don't recognize it, open your banking app directly or call the number printed on your card."

**Analysis:**
```json
{
  "label": "Uncertain",
  "reasoning": "The message recommends safer verification channels and does not ask for credentials, but the text alone cannot confirm who sent it or whether a flagged purchase exists. Verify independently rather than replying to the message.",
  "intent": "Prompt the recipient to review a possible card transaction",
  "risk_factors": ["Sender cannot be verified from the message", "Unconfirmed account activity"]
}
```

## Example 16:
**Message:** "A delivery address issue is holding your package. Reply with your full address and apartment number so we can redirect it."

**Analysis:**
```json
{
  "label": "Uncertain",
  "reasoning": "A courier may need address details to correct a delivery, but the sender is not identified and asks for personal information by reply. The text alone is not enough to confirm whether this is legitimate.",
  "intent": "Collect an address to redirect a delivery, or potentially obtain personal information",
  "risk_factors": ["Unidentified sender", "Request for home address by reply", "Delivery redirection"]
}
```


## Your Task:
Analyze the following message using the same structured approach. Output only the JSON response. 