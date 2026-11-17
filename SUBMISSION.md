
## RAG Evaluation

| Question | Expected Source | Retrieved Filenames | Without RAG | With RAG | Supported by Source? |
|---|---|---|---|---|---|
| How many hours before an appointment must I cancel? | [Appointment policy file] | [cancellations.txt] | [I'm sorry, but I can't answer this question as it doesn't provide enough context. Could you please provide more information or clarify the question?] | [You must cancel your appointment at least 18 hours before the scheduled time.] | [Yes] |
| Can I request a same-day appointment? | [Appointment policy file] | [scheduling.txt] | [I'm sorry, but I can't assist with that.] | [Yes, you can request a same-day appointment, but it must be available.] | [Yes] |
| How are laboratory results communicated? | [Lab results policy file] | [lab_results.txt] | [Laboratory results are typically communicated in several ways, depending on the context and the nature of the results. Here are some common methods: Written Reports: Laboratory results are often reported in written form, either as a report or as part of a larger report. This can be sent to the patient, the referring physician, or the patient's insurance company. Email or Electronic Health Records (EHR): Results can be sent electronically via email or integrated into electronic health records (EHR) systems. This is particularly useful for sharing results with multiple healthcare providers. Phone Calls: Results can be communicated over the phone, especially if the results are urgent or require immediate action. In-Person Consultations: In some cases, results may be discussed in person, either at the patient's request or as part of a follow-up appointment. Notifications: Some laboratories may send notifications via text message or mobile app, especially for results that are not immediately actionable. Patient Education: In some cases, the laboratory may provide educational materials or information about the results, especially if the results are complex or require further explanation. Follow-Up Appointments: Results may be discussed during follow-up appointments, either in person or via telehealth. The method of communication is often determined by the urgency of the results, the preferences of the patient or healthcare provider, and the specific requirements of the laboratory and the healthcare system.] | [Laboratory results are communicated through the secure patient portal.] | [Yes] |
| Does the clinic provide free transportation? | None — unsupported | [None] | [I'm sorry, but I can't answer this question because I don't have any specific information about a particular clinic. The answer would depend on the clinic's policies and the location. If you know the name of the clinic or the location, you can search online or contact them directly to find out if they provide free transportation.] | [I do not have enough information in the provided documents.] | [Yes - correct fallback] |
| What happens when I ask about an unsupported policy? | None — tests fallback behavior | [lab_results.txt, scheduling.txt] | [When you ask about an unsupported policy, it typically means that the policy you are referring to is not supported by the current version of the software, system, or service you are using. This could be due to a variety of reasons, such as the policy being deprecated, removed, or not supported in the current version. In such cases, it is important to check the documentation or support resources for the specific version of the software, system, or service you are using to find out what policies are supported. You may also need to upgrade to a newer version of the software, system, or service to use the policy. If you are unsure about what policies are supported, it is best to consult with the support team or documentation for the specific software, system, or service you are using. They can provide you with the most accurate and up-to-date information on what policies are supported in the current version.] | [When you ask about an unsupported policy, the response is: "I do not have enough information in the provided documents."] | [Yes] |

## Failure Analysis

**Failed question:** What happens when I ask about an unsupported policy?

**Expected:** The chatbot should recognize that the question is not answered by the clinic's policy documents and respond with: "I do not have enough information in the provided documents."

**Actual:** The chatbot retrieved lab_results.txt and scheduling.txt, even though neither document directly answered the question. It then explained what happens when an unsupported policy is requested instead of returning only the fallback message.

**Failure type:** Both retrieval and generation.

**Explanation:** The TF-IDF retrieval system matched words in the question to unrelated documents, resulting in irrelevant context being passed to the LLM. The LLM then generated an explanation rather than following the exact fallback instruction. This shows that retrieving documents does not guarantee they contain the information needed to answer a question.


**Change made:** I strengthened the system prompt in llm.py to instruct the model to return the fallback message when the retrieved documents do not directly answer the question.

**Rerun outcome:** The chatbot returned the exact fallback message instead of generating an unsupported explanation. This improved the generation behavior, although retrieval still selected irrelevant documents.


