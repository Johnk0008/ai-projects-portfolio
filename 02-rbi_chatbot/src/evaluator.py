# src/evaluator.py
import time
import json

class Evaluator:
    def __init__(self):
        pass
    
    def evaluate_chatbot(self, chatbot, test_questions):
        """Evaluate chatbot performance"""
        print("🧪 Starting chatbot evaluation...")
        results = []
        
        for i, test_case in enumerate(test_questions, 1):
            print(f"📋 Test {i}/{len(test_questions)}: {test_case['question']}")
            
            response = chatbot.ask_question(test_case["question"])
            
            result = {
                "test_case": i,
                "question": test_case["question"],
                "expected_answer": test_case["expected_answer"],
                "actual_answer": response["answer"],
                "sources_found": len(response["source_documents"]),
                "success": response["success"],
                "answer_length": len(response["answer"])
            }
            
            results.append(result)
            print(f"   ✅ Response generated: {len(response['answer'])} characters")
            
            # Avoid rate limiting
            time.sleep(1)
        
        return results
    
    def save_results(self, results, filename="evaluation_results.json"):
        """Save evaluation results"""
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        print(f"💾 Evaluation results saved to {filename}")
    
    def print_summary(self, results):
        """Print evaluation summary"""
        print("\n" + "="*60)
        print("📊 EVALUATION SUMMARY")
        print("="*60)
        
        total = len(results)
        successful = sum(1 for r in results if r["success"])
        avg_sources = sum(r["sources_found"] for r in results) / total if total > 0 else 0
        
        print(f"Total Questions: {total}")
        print(f"Successful Responses: {successful}/{total} ({successful/total*100:.1f}%)")
        print(f"Average Sources per Answer: {avg_sources:.1f}")
        
        print("\n📝 Detailed Results:")
        for result in results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"  {status} | Q: {result['question'][:50]}...")