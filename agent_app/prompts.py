from langchain_core.prompts import PromptTemplate

intent_prompt = PromptTemplate.from_template(
    """You are good at classifying a question.
    Given the user question below, classify it as either being about `database`, `chat` or 'off_topic'.

    <If the question is about products of the restaurant OR ordering food classify the question as 'database'>
    <If the question is about restaurant related topics like opening hours and similar topics, classify it as 'chat'>
    <If the question is about whether, football or anything not related to the restaurant or
    products, classify the question as 'off_topic'>

    <question>
    {question}
    </question>

    Classification:"""
)