import sys
import csv
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder, three_to_one
from Bio.PDB.PDBExceptions import PDBConstructionWarning

def fetch_pdb(pdb_id):
    pdb_list = PDB.PDBList()
    filename = pdb_list.retrieve_pdb_file(pdb_id, file_format="pdb")
    return filename

def extract_phi_psi(pdb_id, chain_id):
    parser = PDB.PDBParser(QUIET=True, PERMISSIVE=False)
    structure = parser.get_structure(pdb_id, fetch_pdb(pdb_id))

    if chain_id not in [chain.id for chain in structure[0]]:
        raise ValueError(f"Chain {chain_id} not found in PDB structure.")

    ppb = PPBuilder()
    phi_psi = []

    for pp in ppb.build_peptides(structure[0][chain_id], aa_only=False):
        for residue, angles in zip(pp, pp.get_phi_psi_list()):
            res_name = residue.get_resname()
            res_id = residue.get_id()[1]

            if res_name in PDB.Polypeptide.aa3:
                res_name_1 = three_to_one(res_name)
                phi, psi = angles

                if phi and psi:
                    phi_psi.append([res_name_1, res_id, phi, psi])

    return phi_psi

def write_to_csv(phi_psi_data, output_filename):
    with open(output_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi", "Psi"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    pdb_id = input("Enter PDB ID: ")
    chain_id = input("Enter chain ID: ")
    output_filename = f"{pdb_id}_{chain_id}_phi_psi.csv"

    try:
        phi_psi_data = extract_phi_psi(pdb_id, chain_id)
        write_to_csv(phi_psi_data, output_filename)
        print(f"Phi-Psi angles written to {output_filename}")
    except Exception as e:
        print(f"Error: {str(e)}")
