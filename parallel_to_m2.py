import argparse
import io
import os
import spacy
import scripts.align_text as align_text

# The input files may be tokenized or untokenized.
# Assumption 1: Each line in each file aligns exactly.
# Assumption 2: Each line in each file is at least 1 sentence in orig and cor.
def main(args):
	basename = os.path.dirname(os.path.realpath(__file__))
	print("Loading resources...")
	# Load Tokenizer and other resources
	nlp = spacy.load("en")
	
	# Setup output m2 file based on corrected file name.
	m2_out = open(args.out if args.out.endswith(".m2") else args.out+".m2", "w")

	print("Processing files...")	
	with io.open(args.orig, encoding='utf-8') as orig, io.open(args.cor, encoding='utf-8') as cor:
		# Process each pre-aligned sentence pair.
		for orig_sent, cor_sent in zip(orig, cor):
			# Get the raw text.
			orig_sent = orig_sent.strip()
			cor_sent = cor_sent.strip()
			# Ignore empty sentences
			if not orig_sent and not cor_sent: continue
			# If args.tok, we also need to tokenise the text.
			if args.tok:
				orig_sent = nlp(orig_sent, tag=True, parse=True, entity=False)
				cor_sent = nlp(cor_sent, tag=True, parse=True, entity=False)				
			# Otherwise, assume it is tokenized and then process.
			else:
				orig_sent = nlp.tokenizer.tokens_from_list(orig_sent.split())
				cor_sent = nlp.tokenizer.tokens_from_list(cor_sent.split())
				nlp.tagger(orig_sent)
				nlp.tagger(cor_sent)
				nlp.parser(orig_sent)
				nlp.parser(cor_sent)				
			# Get a list of string toks for each.
			orig_toks = [tok.orth_ for tok in orig_sent]
			cor_toks = [tok.orth_ for tok in cor_sent]				
			# Auto align the sentence and extract the edits.
			auto_edits = align_text.getAutoAlignedEdits(orig_toks, cor_toks, orig_sent, cor_sent, 
														nlp, args.lev, args.merge)
			# Write orig_toks to output.
			m2_out.write("S "+" ".join(orig_toks)+"\n")
			# If there are no edits, write an explicit dummy edit.
			if not auto_edits: m2_out.write("A -1 -1|||noop||||||REQUIRED|||-NONE-|||0\n")
			# Write the auto edits to the file.
			for auto_edit in auto_edits:
				# Write the edit to output.
				m2_out.write(formatEdit(auto_edit)+"\n")
			# Write new line after each sentence.
			m2_out.write("\n")			

# Function to format an edit into M2 output format.
def formatEdit(edit, coder_id=0):
	# edit = [start, end, cat, cor]
	span = " ".join(["A", str(edit[0]), str(edit[1])])
	return "|||".join([span, edit[2], edit[3], "REQUIRED", "-NONE-", str(coder_id)])			


if __name__ == "__main__":
	# Define and parse program input
	parser = argparse.ArgumentParser(description="Convert parallel original and corrected text files (1 sentence per line) into M2 format.\nThe default uses Damerau-Levenshtein and merging rules and assumes tokenized text.",
										formatter_class=argparse.RawTextHelpFormatter,
										usage="%(prog)s [-h] [options] -orig ORIG -cor COR -out OUT")
	parser.add_argument("-orig",
						help="The path to the original text file.",
						required=True)
	parser.add_argument("-cor",
						help="The path to the corrected text file.",
						required=True)
	parser.add_argument("-out",
						help="The full filename of where you want the output m2 file saved.",
						required=True)							
	parser.add_argument("-tok",
						help="Use this flag if the parallel sentences are untokenized.",
						action="store_true")
	parser.add_argument("-lev",
						help="Align texts using standard Levenshtein rather than our linguistically \nenhanced Damerau-Levenshtein distance.",
						action="store_true")
	parser.add_argument("-merge",
						help="Choose a merging strategy for an automatic alignment.\n"
								"all-split: Merge nothing; e.g. MSSDI -> M, S, S, D, I\n"
								"all-merge: Merge adjacent non-matches; e.g. MSSDI -> M, SSDI\n"
								"all-equal: Merge adjacent same-type non-matches; e.g. MSSDI -> M, SS, D, I\n"
								"rules: Use our own rule-based merging strategy (default)",
						default="rules")
	args = parser.parse_args()
	# Run the program.
	main(args)
