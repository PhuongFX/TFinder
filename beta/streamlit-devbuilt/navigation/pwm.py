import streamlit as st
import numpy as np
from weblogo import *
from Bio.Seq import Seq
from weblogo import *

def pwm_page():
    def calculate_pwm(sequences):
        num_sequences = len(sequences)
        sequence_length = len(sequences[0])
        pwm = np.zeros((4, sequence_length))
        for i in range(sequence_length):
            counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
            for sequence in sequences:
                nucleotide = sequence[i]
                if nucleotide in counts:
                    counts[nucleotide] += 1
            pwm[0, i] = counts['A'] / num_sequences *100
            pwm[1, i] = counts['T'] / num_sequences *100
            pwm[2, i] = counts['G'] / num_sequences *100
            pwm[3, i] = counts['C'] / num_sequences *100

        return pwm

    def parse_fasta(fasta_text):
        sequences = []
        current_sequence = ""

        for line in fasta_text.splitlines():
            if line.startswith(">"):
                if current_sequence:
                    sequences.append(current_sequence)
                current_sequence = ""
            else:
                current_sequence += line

        if current_sequence:
            sequences.append(current_sequence)

        return sequences

    st.subheader("🧮 PWM generator")

    fasta_text = st.text_area("Put FASTA sequences. Same sequence length required ⚠️", height=300)
    
    def generate_weblogo(weblogo):
        # Convertir les séquences en format Seq de BioPython
        seqs = [Seq(seq) for seq in weblogo]

        # Créer l'objet LogoOptions
        options = LogoOptions()
        options.logo_title = "WebLogo"
        options.color_scheme = classic

        # Créer l'objet LogoData
        data = LogoData.from_seqs(seqs)

        # Générer le weblogo
        format = LogoFormat(data, options)
        png = png_formatter(data, format)

        return png

    if st.button('Generate PWM'):
        if fasta_text:
            
            sequences = parse_fasta(fasta_text)
            sequences = [seq.upper() for seq in sequences]
            
            weblogo = fasta_text.splitlines()
            
            if weblogo:
                weblogo1 = generate_weblogo(weblogo)
                st.image(weblogo1, use_column_width=True)

            if len(sequences) > 0:
                pwm = calculate_pwm(sequences)

                st.subheader("PWM: ")
                st.info("⬇️ Select and copy")
                bases = ['A', 'T', 'G', 'C']
                pwm_text = ""
                for i in range(len(pwm)):
                    base_name = bases[i]
                    base_values = pwm[i]

                    base_str = base_name + " ["
                    for value in base_values:
                        base_str += "\t" + format(value) + "\t" if np.isfinite(value) else "\t" + "NA" + "\t"

                    base_str += "]\n"
                    pwm_text += base_str

                st.text_area("PWM résultante", value=pwm_text)
                
            else:
                st.warning("You forget FASTA sequences :)")



