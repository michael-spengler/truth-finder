# -*- coding: utf-8 -*-
# +
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"
# -

import pandas as pd
import numpy as np

df_eme_raw = pd.read_csv("data/scraped/emergent_phase2_clean_2018_7_2.csv")
df_poli_raw = pd.read_csv("data/scraped/politifact_phase2_clean_2018_7_3.csv", warn_bad_lines=True, error_bad_lines=False)
df_snopes_raw = pd.read_csv("data/scraped/snopes_phase2_clean_2018_7_3.csv")

df_eme = df_eme_raw.copy()
df_poli = df_poli_raw.copy()
df_snopes = df_snopes_raw.copy()

for df in [df_eme, df_poli, df_snopes]:
    df.head().T

df_poli.original_url_phase1[0]

for df in [df_poli, df_snopes, df_eme]:
    df.columns

df_poli.drop(columns=['politifact_url_phase1','article_title_phase1','article_published_date_phase1','article_researched_by_phase1','article_edited_by_phase1',
                     'original_url_phase1','publish_date_phase2','article_claim_citation_phase1','error_phase2','page_is_first_citation_phase1'],
             inplace=True)
df_snopes.drop(columns=['snopes_url_phase1','article_title_phase1','article_date_phase1','article_origin_url_phase1','publish_date_phase2','error_phase2',
                       'page_is_first_citation_phase1','index_paragraph_phase1'],
               inplace=True)
df_eme.drop(columns=['emergent_url_phase1','article_date_phase1','article_tracking_body_phase1','original_url_phase1',
                     'publish_date_phase2','error_phase2','claim_description_phase1','article_tags_phase1'], 
            inplace=True)

df_poli.rename(columns={'fact_tag_phase1':'label','article_title_phase2':'title','article_claim_phase1':'claim',
                        'article_categories_phase1':'categories', 'original_article_text_phase2':'text',
                        'author_phase2':'author'},
               inplace=True)
df_snopes.rename(columns={'fact_rating_phase1':'label','article_title_phase2':'title', 'article_claim_phase1':'claim',
                          'article_category_phase1':'categories', 'original_article_text_phase2':'text',
                          'author_phase2':'author'},
                 inplace=True)
df_eme.rename(columns={'fact_tag_phase1':'label','article_title_phase2':'title', 'claim_phase1':'claim',
                       'category_phase1':'categories', 'original_article_text_phase2':'text',
                       'author_phase2':'author'},
              inplace=True)

for df in [df_poli, df_snopes, df_eme]:
    df.sort_index(axis=1, inplace=True)

for df in [df_poli, df_snopes, df_eme]:
    df.columns

for df in [df_poli, df_snopes, df_eme]:
    df.head().T

for df in [df_poli, df_snopes, df_eme]:
    df.label.unique()

for df in [df_poli, df_snopes, df_eme]:
    len(df)

df_poli_raw['politifact_url_phase1'][0]

df_eme_raw['emergent_url_phase1'][0]

df_snopes_raw['snopes_url_phase1'][0]

# ## How do Scores work?
#
# ### Politico
# How we determine Truth-O-Meter ratings
# The goal of the Truth-O-Meter is to reflect the relative accuracy of a statement. The meter has six ratings, in decreasing level of truthfulness:
#
# TRUE – The statement is accurate and there’s nothing significant missing.
#
# MOSTLY TRUE – The statement is accurate but needs clarification or additional information.
#
# HALF TRUE – The statement is partially accurate but leaves out important details or takes things out of context.
#
# MOSTLY FALSE – The statement contains an element of truth but ignores critical facts that would give a different impression.
#
# FALSE – The statement is not accurate.
#
# PANTS ON FIRE – The statement is not accurate and makes a ridiculous claim.
#
# The burden of proof is on the speaker, and we rate statements based on the information known at the time the statement is made.
#
# The reporter who researches and writes the fact-check suggests a rating when they turn in the report to an assigning editor. The editor and reporter review the report together, typically making clarifications and adding additional details. They come to agreement on the rating. Then, the assigning editor brings the rated fact-check to two additional editors.
#
# The three editors and reporter then review the fact-check by discussing the following questions.
#
# • Is the statement literally true?
#
# • Is there another way to read the statement? Is the statement open to interpretation?
#
# • Did the speaker provide evidence? Did the speaker prove the statement to be true?
#
# • How have we handled similar statements in the past? What is PolitiFact’s jurisprudence?
#
# The three editors then vote on the rating (two votes carry the decision), sometimes leaving it as the reporter suggested and sometimes changing it to a different rating. More edits are made; the report is then published.
#
#
# ### Snopes
#
# True: This rating indicates that the primary elements of a claim are demonstrably true.
#
# Mostly True: This rating indicates that the primary elements of a claim are demonstrably true, but some of the ancillary details surrounding the claim may be inaccurate.
#
# Mixture: This rating indicates that a claim has significant elements of both truth and falsity to it such that it could not fairly be described by any other rating.
#
# Mostly False: This rating indicates that the primary elements of a claim are demonstrably false, but some of the ancillary details surrounding the claim may be accurate.
#
# False: This rating indicates that the primary elements of a claim are demonstrably false.
#
# Unproven: This rating indicates that insufficient evidence exists to establish the given claim as true, but the claim cannot be definitively proved false. This rating typically involves claims for which there is little or no affirmative evidence, but for which declaring them to be false would require the difficult (if not impossible) task of our being able to prove a negative or accurately discern someone else’s thoughts and motivations.
#
# Miscaptioned: This rating is used with photographs and videos that are “real” (i.e., not the product, partially or wholly, of digital manipulation) but are nonetheless misleading because they are accompanied by explanatory material that falsely describes their origin, context, and/or meaning.
# [no information from photos, should look further into this]
#
# Correct Attribution: This rating indicates that quoted material (speech or text) has been correctly attributed to the person who spoke or wrote it. 
# [add this too 'true' ?]
#
# Misattributed: This rating indicates that quoted material (speech or text) has been incorrectly attributed to a person who didn’t speak or write it.
# [needs to be filtered, there is no fact checking from our side, worsens training data]
#
# Legend: This rating is most commonly associated with items that describe events so general or lacking in detail that they could have happened to someone, somewhere, at some time, and are therefore essentially unprovable.
#
# Outdated: This rating applies to items for which subsequent events have rendered their original truth rating irrelevant (e.g., a condition that was the subject of protest has been rectified, or the passage of a controversial law has since been repealed). [needs to be filtered, can be true or false, cant be determined by writing style]
#
# Scam: This “rating” is not a truth rating but rather indicates pages that describe the details of verified scams.




