from transformers import pipeline
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
text = "At the close of 2021 a popular Seeking Alpha contributor posted an  detailing why she believed that oil would experience a big move up in the 2020s decade setting the stage for what she callsStill in late 2021 I had arrived at the same basic conclusion a change in the energy sector is upon us and will dramatically take shape and shape fortunes throughout thisRegarding the longterm future of the energy sector my viewpoint is based on the following phenomena and developmentsBecause of these developments I believe that the energy boom in the aftermath of the RussiaUkraine conflict marks the last time that oil and other fossil fuels can be relied upon to enrich contemporary energy companies that comprise much of the energy sector today In my opinion these companies as well as their investors would be wise to transition away from fossil fuels as soon as possible during the 2020sIn the following sections I will explain in detail why I believe that this decade represents the last age of oil while also exploring how this affects one of the worlds largest and most vertically integrated oil companies Exxon Mobil Corporation After the forced breakup of Standard Oil an American oil behemoth Exxon became one of the most successful divisions to be spun off the company Exxon is among the largest privately owned and publicly traded oil companies in the world and produces a large amount of the worlds energy  in 2018"
model_name = "facebook/bart-large-cnn"
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(model_name)
inputs = tokenizer(text, return_tensors="pt").input_ids
from transformers import AutoModelForSeq2SeqLM

# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
# outputs = model.generate(inputs, max_new_tokens=50, do_sample=False)
# result = tokenizer.decode(outputs[0], skip_special_tokens=True)
# print("pytorch:",result)
# summarizer = pipeline("summarization", model=model_name, max_length =100, )
# summary = summarizer(text)
# print("pipeline:",summary[0]['summary_text'])
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

ARTICLE = """ New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.
Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the
2010 marriage license application, according to court documents.
Prosecutors said the marriages were part of an immigration scam.
On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective
Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s
Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18.
"""
print(summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False))
