from groq import Groq
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

# initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def rank_candidates_with_llm(query, ranked_candidates):
    """
    Takes HR query and ranked candidates from Module 4.
    Uses Groq/Llama to analyze and explain each candidate's fit.
    Returns enriched candidate list with AI explanation.
    """

    results = []

    for candidate in ranked_candidates:
        name       = candidate["name"]
        best_score = candidate["best_score"]
        chunks     = candidate["chunks"]

        # combine all chunks into one resume text
        resume_text = "\n\n".join(chunks)

        # build the prompt
        prompt = f"""
You are an expert HR assistant helping shortlist candidates.

Job Requirement:
{query}

Candidate Name: {name}
Match Score: {best_score}/100

Resume Content:
{resume_text}

Based on the resume content and job requirement, provide:
1. A brief analysis (2-3 sentences) of why this candidate is or isn't a good fit
2. Key matching skills found in the resume
3. Key missing skills based on the job requirement
4. A final recommendation: STRONGLY RECOMMENDED / RECOMMENDED / NOT RECOMMENDED

Keep your response concise and structured.
"""

        print(f"\nAnalyzing candidate: {name}...")

        # call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # fast and free
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert HR assistant who analyzes resumes and provides structured candidate evaluations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,   # lower = more consistent, focused output
            max_tokens=500     # keep responses concise
        )

        # extract the text response
        analysis = response.choices[0].message.content

        # add analysis to candidate result
        results.append({
            "name":     name,
            "score":    best_score,
            "analysis": analysis,
            "chunks":   chunks
        })

    return results


def display_results(results):
    """
    Prints final shortlist results in a clean readable format.
    """
    print("\n" + "="*60)
    print("         FINAL HR SHORTLIST REPORT")
    print("="*60)

    for rank, candidate in enumerate(results, 1):
        print(f"\nRank #{rank} — {candidate['name']}")
        print(f"Match Score : {candidate['score']} / 100")
        print(f"\nAI Analysis:")
        print(candidate['analysis'])
        print("-"*60)


# test block
if __name__ == "__main__":
    from retrieval import get_candidate_results, collection

    # check chunks in DB
    count = collection.count()
    print(f"Total chunks in DB: {count}")

    # HR query
    query = "Python machine learning developer with project experience"

    # get ranked candidates from Module 4
    ranked_candidates = get_candidate_results(query, top_k=count)

    # run LLM ranking
    final_results = rank_candidates_with_llm(query, ranked_candidates)

    # display
    display_results(final_results)