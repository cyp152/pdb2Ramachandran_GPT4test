# pdb2Ramachandran_GPT4test

2023年3月9日にPythonのライトユーザーがChatGPT4にお願いして
pythonスクリプトを作成できるか試した実行記録です。
以下、やり取りをそのままコピペしました。気が向いたらきれいにまとめます。
余裕があれば、途中のpytonファイルを保存しているのでアップします。

--

<img src="https://user-images.githubusercontent.com/87903303/226152460-1a22e58e-d9dc-47dc-9eb1-82972e9ae910.png　width="5%" />
PDBIDとchain番号を入力すると、1残基ずつタンパク質構造中のアミノ酸残基1文字表記と主鎖二面角φとψをcsv形式で出力するpythonスクリプトを作成してください。

--

以下に、PDBファイルのIDとチェーン番号を入力して、タンパク質構造中のアミノ酸残基の1文字表記と主鎖二面角φ(Phi)とψ(Psi)をCSV形式で出力するPythonスクリプトを示します。このスクリプトでは、BioPythonライブラリを使用しています。BioPythonをインストールしていない場合は、pip install biopythonでインストールしてください。

```
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

            if res_name in PDB.Polypeptide.three_to_one:
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
        
```

このスクリプトを実行すると、PDB IDとチェーンIDを入力するプロンプトが表示されます。入力すると、CSVファイルにアミノ酸残基の1文字表記と主鎖二面角φとψが出力されます。CSVファイルの名前は、PDBID_chainID_phi_psi.csvとなります。

--

Enter PDB ID: 5yhj
Enter chain ID: B
Structure exists: 'C:\Users\xxxxxxx\Desktop\yh\pdb5yhj.ent' 
Error: argument of type 'function' is not iterable

このようなエラーが出ました。この問題を解決する改善策を教えてください。

---

すみません、この問題は、if res_name in PDB.Polypeptide.three_to_one行に原因があります。PDB.Polypeptide.three_to_one は関数ですが、ここではリストやセットとして扱われています。これを修正するには、PDB.Polypeptide.three_to_one を PDB.Polypeptide.aa3 に置き換えて、アミノ酸名が有効かどうかを確認します。

修正後のコードは以下のようになります。

--

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
        
--

これで、エラーが解決され、アミノ酸残基と主鎖二面角をCSVファイルに出力できるはずです。

--

弧度法から度数法に変換して出力してください。

--

Pythonのmath.degrees()関数を使って、弧度法から度数法に変換できます。以下に、修正済みのスクリプトを示します。

--

import sys
import csv
import math
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
                    phi_degrees = math.degrees(phi)
                    psi_degrees = math.degrees(psi)
                    phi_psi.append([res_name_1, res_id, phi_degrees, psi_degrees])

    return phi_psi

def write_to_csv(phi_psi_data, output_filename):
    with open(output_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
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
        
--

この修正済みのスクリプトでは、math.degrees()を使って弧度法から度数法に変換し、CSVファイルに出力される角度が度数法で表示されます。

--

PDB形式とPDBx/mmCIF形式に対応させてください。

--

BioPythonライブラリは、PDBx/mmCIF形式のファイルもサポートしています。以下のスクリプトは、PDB形式とPDBx/mmCIF形式の両方に対応しています。

--

import sys
import csv
import math
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder, three_to_one
from Bio.PDB.PDBExceptions import PDBConstructionWarning

def fetch_pdb(pdb_id, file_format):
    pdb_list = PDB.PDBList()
    filename = pdb_list.retrieve_pdb_file(pdb_id, pdir=".", file_format=file_format)
    return filename

def extract_phi_psi(pdb_id, chain_id, file_format):
    if file_format == "pdb":
        parser = PDB.PDBParser(QUIET=True, PERMISSIVE=False)
    elif file_format == "cif":
        parser = PDB.MMCIFParser(QUIET=True, PERMISSIVE=False)
    else:
        raise ValueError("Invalid file format. Choose either 'pdb' or 'cif'.")

    structure = parser.get_structure(pdb_id, fetch_pdb(pdb_id, file_format))

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
                    phi_degrees = math.degrees(phi)
                    psi_degrees = math.degrees(psi)
                    phi_psi.append([res_name_1, res_id, phi_degrees, psi_degrees])

    return phi_psi

def write_to_csv(phi_psi_data, output_filename):
    with open(output_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    pdb_id = input("Enter PDB ID: ")
    chain_id = input("Enter chain ID: ")
    file_format = input("Enter file format (pdb or cif): ")
    output_filename = f"{pdb_id}_{chain_id}_phi_psi.csv"

    try:
        phi_psi_data = extract_phi_psi(pdb_id, chain_id, file_format)
        write_to_csv(phi_psi_data, output_filename)
        print(f"Phi-Psi angles written to {output_filename}")
    except Exception as e:
        print(f"Error: {str(e)}")
--

この修正済みのスクリプトでは、ファイル形式（pdbまたはcif）も入力するようになっており、選択した形式のファイルをダウンロードして解析します。PDB形式とPDBx/mmCIF形式のどちらのファイルでも、アミノ酸残基と主

--

pdbのファイル形式は問題が発生しませんでしたが、cifでは下記のようなエラーが出ました。改善策を教えてください。
※誤ってエラーを打ち込む前にエンターを押してしまいました。

--

エラーメッセージが提供されていないため、具体的な問題に対処することはできませんが、一般的な問題に対処するために、以下の改善策を提案します。

BioPythonの最新バージョンを使用していることを確認してください。バージョンが古い場合、最新バージョンにアップグレードしてください。以下のコマンドでアップグレードできます。

pip install --upgrade biopython

PDBx/mmCIF形式のファイルには、アミノ酸名が3文字ではなく、大文字の3文字表記になっている場合があります。これに対処するには、res_nameを大文字に変換することで、コードを修正します。

res_name = residue.get_resname().upper()

これらの変更を加えた後、再度スクリプトを実行して、問題が解決するかどうか確認してください。もしまだ問題が解決しない場合は、エラーメッセージを提供していただければ、問題の特定と解決策の提案ができるかもしれません。

--

pdbのファイル形式は問題が発生しませんでしたが、cifでは下記のようなエラーが出ました。改善策を教えてください。

--

Enter PDB ID: 5yhj
Enter chain ID: B
Enter file format (pdb or cif): pdb
Structure exists: '.\pdb5yhj.ent' 

Warning (from warnings module):
  File "C:\Users\xxxx\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\Bio\PDB\Polypeptide.py", line 144
    warnings.warn(
BiopythonDeprecationWarning: 'three_to_one' will be deprecated in a future release of Biopython in favor of 'Bio.PDB.Polypeptide.protein_letters_3to1'.
Phi-Psi angles written to 5yhj_B_phi_psi.csv

=================== RESTART: C:/Users/xxxxxx/Desktop/rama3.py ===================
Enter PDB ID: 5yhj
Enter chain ID: B
Enter file format (pdb or cif): cif
Error: MMCIFParser.__init__() got an unexpected keyword argument 'PERMISSIVE'

--

このエラーは、MMCIFParserの__init__()関数に、予期しないキーワード引数PERMISSIVEが渡されているために発生しています。PDBParserにはPERMISSIVEという引数がありますが、MMCIFParserには存在しないため、このエラーが発生しています。

この問題を解決するには、MMCIFParserのインスタンス化時にPERMISSIVE引数を削除してください。以下に修正後のコードを示します。

--
import sys
import csv
import math
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder, three_to_one
from Bio.PDB.PDBExceptions import PDBConstructionWarning

def fetch_pdb(pdb_id, file_format):
    pdb_list = PDB.PDBList()
    filename = pdb_list.retrieve_pdb_file(pdb_id, pdir=".", file_format=file_format)
    return filename

def extract_phi_psi(pdb_id, chain_id, file_format):
    if file_format == "pdb":
        parser = PDB.PDBParser(QUIET=True, PERMISSIVE=False)
    elif file_format == "cif":
        parser = PDB.MMCIFParser(QUIET=True)
    else:
        raise ValueError("Invalid file format. Choose either 'pdb' or 'cif'.")

    structure = parser.get_structure(pdb_id, fetch_pdb(pdb_id, file_format))

    if chain_id not in [chain.id for chain in structure[0]]:
        raise ValueError(f"Chain {chain_id} not found in PDB structure.")

    ppb = PPBuilder()
    phi_psi = []

    for pp in ppb.build_peptides(structure[0][chain_id], aa_only=False):
        for residue, angles in zip(pp, pp.get_phi_psi_list()):
            res_name = residue.get_resname().upper()
            res_id = residue.get_id()[1]

            if res_name in PDB.Polypeptide.aa3:
                res_name_1 = three_to_one(res_name)
                phi, psi = angles

                if phi and psi:
                    phi_degrees = math.degrees(phi)
                    psi_degrees = math.degrees(psi)
                    phi_psi.append([res_name_1, res_id, phi_degrees, psi_degrees])

    return phi_psi

def write_to_csv(phi_psi_data, output_filename):
    with open(output_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    pdb_id = input("Enter PDB ID: ")
    chain_id = input("Enter chain ID: ")
    file_format = input("Enter file format (pdb or cif): ")
    output_filename = f"{pdb_id}_{chain_id}_phi_psi.csv"

    try:
        phi_psi_data = extract_phi_psi(pdb_id, chain_id, file_format)
        write_to_csv(phi_psi_data, output_filename)
        print(f"Phi-Psi angles written to {output_filename}")
    except Exception as e:
        print(f"Error: {str(e)}")

--

下記のようなエラーで止まってしまいました。改善策を教えてください。

Enter PDB ID: 5yhj
Enter chain ID: B
Enter file format (pdb or cif): cif
Error: 'cif'

--

エラーが発生する原因は、fetch_pdb()関数がfile_formatを正しく解釈できていないためです。retrieve_pdb_file()関数のfile_format引数には、"pdb"または"mmCIF"を使用する必要があります。以下に修正後のスクリプトを示します。

--

import sys
import csv
import math
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder, three_to_one
from Bio.PDB.PDBExceptions import PDBConstructionWarning

def fetch_pdb(pdb_id, file_format):
    pdb_list = PDB.PDBList()
    if file_format == "cif":
        file_format = "mmCIF"
    filename = pdb_list.retrieve_pdb_file(pdb_id, pdir=".", file_format=file_format)
    return filename

def extract_phi_psi(pdb_id, chain_id, file_format):
    if file_format == "pdb":
        parser = PDB.PDBParser(QUIET=True, PERMISSIVE=False)
    elif file_format == "cif":
        parser = PDB.MMCIFParser(QUIET=True)
    else:
        raise ValueError("Invalid file format. Choose either 'pdb' or 'cif'.")

    structure = parser.get_structure(pdb_id, fetch_pdb(pdb_id, file_format))

    if chain_id not in [chain.id for chain in structure[0]]:
        raise ValueError(f"Chain {chain_id} not found in PDB structure.")

    ppb = PPBuilder()
    phi_psi = []

    for pp in ppb.build_peptides(structure[0][chain_id], aa_only=False):
        for residue, angles in zip(pp, pp.get_phi_psi_list()):
            res_name = residue.get_resname().upper()
            res_id = residue.get_id()[1]

            if res_name in PDB.Polypeptide.aa3:
                res_name_1 = three_to_one(res_name)
                phi, psi = angles

                if phi and psi:
                    phi_degrees = math.degrees(phi)
                    psi_degrees = math.degrees(psi)
                    phi_psi.append([res_name_1, res_id, phi_degrees, psi_degrees])

    return phi_psi

def write_to_csv(phi_psi_data, output_filename):
    with open(output_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    pdb_id = input("Enter PDB ID: ")
    chain_id = input("Enter chain ID: ")
    file_format = input("Enter file format (pdb or cif): ")
    output_filename = f"{pdb_id}_{chain_id}_phi_psi.csv"

    try:
        phi_psi_data = extract_phi_psi(pdb_id, chain_id, file_format)
        write_to_csv(phi_psi_data, output_filename)
        print(f"Phi-Psi angles written to {output_filename}")
    except Exception as e:
        print(f"Error: {str(e)}")
 
--

この修正後のスクリプトでは、fetch_pdb()関数でfile_formatを"mmCIF"に変更しています。これで、PDBx/mmCIF形式のファイルを正

--

下記のようなエラーが出ました解決策が分かれば教えてください。
Enter PDB ID: 5yhj
Enter chain ID: B
Enter file format (pdb or cif): cif
Error: 'mmCIF'

--

すみませんが、このエラーメッセージだけでは問題の原因を特定するのが難しいです。しかし、一般的な問題に対処するために、以下の提案を試してください。

--

pdb_list.retrieve_pdb_file()を使って、ファイル形式がPDBかmmCIFかに関係なく、ファイルをダウンロードできるようにしてみましょう。具体的には、pdb_list.retrieve_pdb_file(pdb_id, pdir=".", file_format=file_format)の呼び出しをpdb_list.retrieve_pdb_file(pdb_id, pdir=".")に変更します。

次に、ファイル形式がPDBかmmCIFかを自動的に判断するようにします。これは、ファイル名の拡張子を確認することで実現できます。

以下に修正後のコードを示します。

--

import sys
import csv
import math
import os
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder, three_to_one
from Bio.PDB.PDBExceptions import PDBConstructionWarning

def fetch_pdb(pdb_id):
    pdb_list = PDB.PDBList()
    filename = pdb_list.retrieve_pdb_file(pdb_id, pdir=".")
    return filename

def extract_phi_psi(pdb_id, chain_id, filename):
    file_format = os.path.splitext(filename)[1]
    if file_format == ".ent":
        parser = PDB.PDBParser(QUIET=True, PERMISSIVE=False)
    elif file_format == ".cif":
        parser = PDB.MMCIFParser(QUIET=True)
    else:
        raise ValueError("Invalid file format. Use either '.ent' (PDB) or '.cif' (mmCIF).")

    structure = parser.get_structure(pdb_id, filename)

    if chain_id not in [chain.id for chain in structure[0]]:
        raise ValueError(f"Chain {chain_id} not found in PDB structure.")

    ppb = PPBuilder()
    phi_psi = []

    for pp in ppb.build_peptides(structure[0][chain_id], aa_only=False):
        for residue, angles in zip(pp, pp.get_phi_psi_list()):
            res_name = residue.get_resname().upper()
            res_id = residue.get_id()[1]

            if res_name in PDB.Polypeptide.aa3:
                res_name_1 = three_to_one(res_name)
                phi, psi = angles

                if phi and psi:
                    phi_degrees = math.degrees(phi)
                    psi_degrees = math.degrees(psi)
                    phi_psi.append([res_name_1, res_id, phi_degrees, psi_degrees])

    return phi_psi

def write_to_csv(phi_psi_data, output_filename):
    with open(output_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    pdb_id = input("Enter PDB ID: ")
    chain_id = input("Enter chain ID: ")
    output_filename = f
（※上限）

--

if __name__ == "__main__":以降を再度記述してください。

--

すみません、コードが途中で切れてしまいました。以下に、if __name__ == "__main__":以降のコードを再度記述します。

--

if __name__ == "__main__":
    pdb_id = input("Enter PDB ID: ")
    chain_id = input("Enter chain ID: ")
    output_filename = f"{pdb_id}_{chain_id}_phi_psi.csv"

    try:
        filename = fetch_pdb(pdb_id)
        phi_psi_data = extract_phi_psi(pdb_id, chain_id, filename)
        write_to_csv(phi_psi_data, output_filename)
        print(f"Phi-Psi angles written to {output_filename}")
    except Exception as e:
        print(f"Error: {str(e)}")
        
--

この修正後のスクリプトでは、fetch_pdb()関数はPDB IDを引数にとり、ファイル形式に関係なくファイルをダウンロードします。その後、extract_phi_psi()関数はファイル名の拡張子を確認し、適切なパーサを使用して構造データを解析します。

--

ありがとうございました。ちなみにこの警告が発生しないような改善策はありますか？
Warning (from warnings module):
  File "C:\Users\xxxxx\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\Bio\PDB\Polypeptide.py", line 144
    warnings.warn(
BiopythonDeprecationWarning: 'three_to_one' will be deprecated in a future release of Biopython in favor of 'Bio.PDB.Polypeptide.protein_letters_3to1'.

--

警告は、将来のBiopythonリリースでthree_to_one関数が非推奨になり、代わりにBio.PDB.Polypeptide.protein_letters_3to1が推奨されることを示しています。警告を解消するには、three_to_oneの代わりにprotein_letters_3to1を使うようにコードを変更します。以下に修正後のコードを示します。

コードの変更点:

from Bio.PDB.Polypeptide import PPBuilder, three_to_one を from Bio.PDB.Polypeptide import PPBuilder, protein_letters_3to1 に変更
res_name_1 = three_to_one(res_name) を res_name_1 = protein_letters_3to1[res_name] に変更
修正後のコード：

--

import sys
import csv
import math
import os
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder, protein_letters_3to1
from Bio.PDB.PDBExceptions import PDBConstructionWarning

def fetch_pdb(pdb_id):
    pdb_list = PDB.PDBList()
    filename = pdb_list.retrieve_pdb_file(pdb_id, pdir=".")
    return filename

def extract_phi_psi(pdb_id, chain_id, filename):
    file_format = os.path.splitext(filename)[1]
    if file_format == ".ent":
        parser = PDB.PDBParser(QUIET=True, PERMISSIVE=False)
    elif file_format == ".cif":
        parser = PDB.MMCIFParser(QUIET=True)
    else:
        raise ValueError("Invalid file format. Use either '.ent' (PDB) or '.cif' (mmCIF).")

    structure = parser.get_structure(pdb_id, filename)

    if chain_id not in [chain.id for chain in structure[0]]:
        raise ValueError(f"Chain {chain_id} not found in PDB structure.")

    ppb = PPBuilder()
    phi_psi = []

    for pp in ppb.build_peptides(structure[0][chain_id], aa_only=False):
        for residue, angles in zip(pp, pp.get_phi_psi_list()):
            res_name = residue.get_resname().upper()
            res_id = residue.get_id()[1]

            if res_name in PDB.Polypeptide.aa3:
                res_name_1 = protein_letters_3to1[res_name]
                phi, psi = angles

                if phi and psi:
                    phi_degrees = math.degrees(phi)
                    psi_degrees = math.degrees(psi)
                    phi_psi.append([res_name_1, res_id, phi_degrees, psi_degrees])

    return phi_psi

def write_to_csv(phi_psi_data, output_filename):
    with open(output_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    pdb_id = input("Enter PDB ID: ")
    chain_id = input("Enter chain ID: ")
    output_filename = f"{pdb_id}_{chain_id}_phi_psi.csv"

    try:
        filename = fetch_pdb(pdb_id)
        phi_psi_data = extract_phi_psi(pdb_id
（※文字数上限）

--

if __name__ == "__main__":以降を記載してください。

--

すみません、再度コードが切れてしまいました。if __name__ == "__main__":以降を記載します。

--

if __name__ == "__main__":
    pdb_id = input("Enter PDB ID: ")
    chain_id = input("Enter chain ID: ")
    output_filename = f"{pdb_id}_{chain_id}_phi_psi.csv"

    try:
        filename = fetch_pdb(pdb_id)
        phi_psi_data = extract_phi_psi(pdb_id, chain_id, filename)
        write_to_csv(phi_psi_data, output_filename)
        print(f"Phi-Psi angles written to {output_filename}")
    except Exception as e:
        print(f"Error: {str(e)}")
--

この修正後のスクリプトでは、非推奨のthree_to_one関数の代わりに、protein_letters_3to1辞書を使用しています。これにより、警告が解消されるはずです。

--

pdb_idとchain_idをテキストボックスで受け取り、下のテキストボックスにPDB形式の出力を表示し、右のテキストボックスにタンパク質構造中のアミノ酸残基の1文字表記と主鎖二面角φ(Phi)とψ(Psi)をCSV形式で表示するGUIを作成してください。

--

PythonのTkinterを使って、指定された機能を持つGUIアプリケーションを作成できます。以下に、コードを示します。

--

import tkinter as tk
from tkinter import ttk
from io import StringIO
import csv

# ここに、以前に提供したfetch_pdb、extract_phi_psi、およびwrite_to_csv関数を含めます。

def run_analysis():
    pdb_id = pdb_id_entry.get()
    chain_id = chain_id_entry.get()

    try:
        filename = fetch_pdb(pdb_id)
        phi_psi_data = extract_phi_psi(pdb_id, chain_id, filename)

        pdb_text.delete('1.0', tk.END)
        with open(filename, "r") as f:
            pdb_text.insert(tk.END, f.read())

        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

        csv_text.delete('1.0', tk.END)
        csv_text.insert(tk.END, csv_output.getvalue())

    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

app = tk.Tk()
app.title("PDB Phi-Psi Analyzer")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

pdb_id_label = ttk.Label(frame, text="PDB ID:")
pdb_id_label.grid(row=0, column=0, sticky=tk.W)
pdb_id_entry = ttk.Entry(frame, width=10)
pdb_id_entry.grid(row=0, column=1, sticky=tk.W)

chain_id_label = ttk.Label(frame, text="Chain ID:")
chain_id_label.grid(row=1, column=0, sticky=tk.W)
chain_id_entry = ttk.Entry(frame, width=10)
chain_id_entry.grid(row=1, column=1, sticky=tk.W)

analyze_button = ttk.Button(frame, text="Analyze", command=run_analysis)
analyze_button.grid(row=2, column=0, columnspan=2, pady=10)

pdb_text = tk.Text(app, wrap=tk.NONE, width=80, height=20)
pdb_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

csv_text = tk.Text(app, wrap=tk.NONE, width=80, height=20)
csv_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

error_label = ttk.Label(app, text="", foreground="red")
error_label.grid(row=2, column=0, columnspan=2, pady=10)

app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)
app.rowconfigure(1, weight=1)

app.mainloop()

--

このコードは、Tkinterを使用して、PDB IDとチェーンIDを入力できるテキストボックス、アナライズボタン、および2つのテキストボックス（1つはPDB形式の出力を表示し、もう1つはCSV形式でφとψの角度を表示）で構成されたGUIを作成します。アナライズボタンをクリックすると、以前に提

--

PDB形式の出力とCSV形式でφとψの角度を表示するテキストボックスにスクロールバーを追加してください。また、φとψの角度を表示するテキストボックスの下にcsvファイルを保存するボタンを作成してください。

--

以下に、指定された変更を加えたコードを示します。

--

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from io import StringIO
import csv

# 以前に提供したfetch_pdb、extract_phi_psi、およびwrite_to_csv関数をここに含めます。

def run_analysis():
    pdb_id = pdb_id_entry.get()
    chain_id = chain_id_entry.get()

    try:
        filename = fetch_pdb(pdb_id)
        phi_psi_data = extract_phi_psi(pdb_id, chain_id, filename)

        pdb_text.delete('1.0', tk.END)
        with open(filename, "r") as f:
            pdb_text.insert(tk.END, f.read())

        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

        csv_text.delete('1.0', tk.END)
        csv_text.insert(tk.END, csv_output.getvalue())

    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

def save_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if file_path:
        with open(file_path, "w") as f:
            f.write(csv_text.get("1.0", tk.END))

app = tk.Tk()
app.title("PDB Phi-Psi Analyzer")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

pdb_id_label = ttk.Label(frame, text="PDB ID:")
pdb_id_label.grid(row=0, column=0, sticky=tk.W)
pdb_id_entry = ttk.Entry(frame, width=10)
pdb_id_entry.grid(row=0, column=1, sticky=tk.W)

chain_id_label = ttk.Label(frame, text="Chain ID:")
chain_id_label.grid(row=1, column=0, sticky=tk.W)
chain_id_entry = ttk.Entry(frame, width=10)
chain_id_entry.grid(row=1, column=1, sticky=tk.W)

analyze_button = ttk.Button(frame, text="Analyze", command=run_analysis)
analyze_button.grid(row=2, column=0, columnspan=2, pady=10)

pdb_text = tk.Text(app, wrap=tk.NONE, width=80, height=20)
pdb_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

pdb_scroll = ttk.Scrollbar(app, orient="vertical", command=pdb_text.yview)
pdb_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
pdb_text.config(yscrollcommand=pdb_scroll.set)

csv_text = tk.Text(app, wrap=tk.NONE, width=80, height=20)
csv_text.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))

csv_scroll = ttk.Scrollbar(app, orient="vertical", command=csv_text.yview)
csv_scroll.grid(row=1, column=3, sticky=(tk.N, tk.S))
csv_text.config(yscrollcommand=csv_scroll.set)

error_label = ttk.Label(app, text="", foreground="red")
error_label.grid(row=2, column=0, columnspan=2, pady=10)

save_button = ttk.Button(app, text="Save CSV", command=save_csv)
save_button.grid(row=2

--

save_button = ttk.Button(app, text="Save CSV", command=save_csv)以降を記載してください。

--

申し訳ありません。コードが途中で切れてしまいました。save_button = ttk.Button(app, text="Save CSV", command=save_csv)以降を記載します。

--

save_button = ttk.Button(app, text="Save CSV", command=save_csv)
save_button.grid(row=2, column=2, pady=10)

app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=0)
app.columnconfigure(2, weight=1)
app.columnconfigure(3, weight=0)
app.rowconfigure(1, weight=1)

app.mainloop()

--

このコードは、save_buttonをアプリケーションの下部に表示し、CSV形式のφとψの角度データを保存するために使用できます。また、pdb_textとcsv_textのテキストボックスにスクロールバーが追加されています。

--

下記のようなエラーが発生しました。何が原因でしょうか。
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.10_3.10.2800.0_x64__qbz5n2kfra8p0\lib\tkinter\__init__.py", line 1921, in __call__
    return self.func(*args)
  File "C:/Users/xxxxx/Desktop/rama6_GUI.py", line 82, in save_csv
    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
NameError: name 'filedialog' is not defined

--

エラーメッセージによれば、filedialogモジュールが定義されていないため、問題が発生しています。tkinterからfiledialogをインポートするのを忘れていたようです。以下のようにfrom tkinter import filedialogをインポートセクションに追加してください。

--

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from io import StringIO
import csv

# 以前に提供したfetch_pdb、extract_phi_psi、およびwrite_to_csv関数をここに含めます。

# 以下のコードは変更なしで続けます。

--

この変更により、filedialogが正しくインポートされ、asksaveasfilename関数を使用できるようになります。

--

私がimportを追記するのを忘れていたようです。Save CSVボタンを押したときに、ファイルの種類をcsvに、標準のファイル名をpdb_id+"_"+chain_idにすることは可能でしょうか。

--

もちろん可能です。save_csv関数を以下のように変更して、ファイルの種類をCSVにし、標準のファイル名をpdb_idとchain_idを組み合わせたものにしてください。

--

def save_csv():
    pdb_id = pdb_id_entry.get()
    chain_id = chain_id_entry.get()
    default_filename = f"{pdb_id}_{chain_id}.csv"
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile=default_filename)
    if file_path:
        with open(file_path, "w") as f:
            f.write(csv_text.get("1.0", tk.END))
            
--

この変更により、Save CSVボタンを押すと、ファイルの種類がCSVに設定され、標準のファイル名がpdb_idとchain_idの組み合わせになります。

--

Excelで開くと行が飛んでしまいます。原因は何でしょうか。

Residue	Residue_ID	Phi (degrees)	Psi (degrees)
			
K	3	-114.0727644	160.4397534
			
V	4	-98.86508471	137.5782105
			
I	5	-79.94903572	124.7772432

--

Excelで開いたときに行が飛んでいる原因は、CSVデータに改行コードが2つ連続して含まれているためです。CSVデータを生成するStringIOオブジェクトに書き込む際、csv_writerが各行の末尾に改行コードを自動的に追加します。したがって、csv_text.insert(tk.END, csv_output.getvalue())の代わりに、以下のように改行コードを削除してからテキストボックスに挿入することができます。

--

        csv_text.delete('1.0', tk.END)
        csv_output_str = csv_output.getvalue().replace('\r\n', '\n').replace('\r', '\n')
        csv_text.insert(tk.END, csv_output_str)
        
--

この変更により、CSVデータの改行コードが正しくなり、Excelで開いたときに行が飛ばなくなります。

--

Phi (degrees),Psi (degrees)のcsv出力時、小数点以下2桁で丸めることは可能でしょうか。また、右側にPhi (degrees),Psi (degrees)の散布図を表示することは可能でしょうか。

--

もちろん可能です。まず、PhiとPsiの角度を小数点以下2桁に丸めるために、write_to_csv関数を以下のように変更します。

--

def write_to_csv(phi_psi_data, csv_output):
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])

    for residue_data in phi_psi_data:
        residue_name = residue_data[0]
        residue_id = residue_data[1]
        phi = round(residue_data[2], 2)  # 丸める
        psi = round(residue_data[3], 2)  # 丸める
        csv_writer.writerow([residue_name, residue_id, phi, psi])
        
--

次に、散布図を表示するために、matplotlibをインポートし、新しい関数plot_scatterを作成します。

--

import matplotlib.pyplot as plt

def plot_scatter(phi_psi_data):
    phi = [round(data[2], 2) for data in phi_psi_data]
    psi = [round(data[3], 2) for data in phi_psi_data]
    
    plt.scatter(phi, psi)
    plt.xlabel('Phi (degrees)')
    plt.ylabel('Psi (degrees)')
    plt.title('Phi-Psi Scatter Plot')
    plt.show()
--

最後に、fetch_buttonが押されたときに、plot_scatter関数を呼び出すようにfetch_pdb関数を変更します。

--

def fetch_pdb():
    # 以前のコード
    phi_psi_data = extract_phi_psi(pdb_id, chain_id, structure)
    write_to_csv(phi_psi_data, csv_output)
    
    csv_text.delete('1.0', tk.END)
    csv_output_str = csv_output.getvalue().replace('\r\n', '\n').replace('\r', '\n')
    csv_text.insert(tk.END, csv_output_str)
    
    plot_scatter(phi_psi_data)  # これを追加

--

これで、PhiとPsiの角度が小数点以下2桁に丸められ、右側に散布図が表示されるようになります。ただし、散布図をTkinterウィンドウ内に埋め込む方法がありますが、ここでは簡単のために別ウィンドウに表示しています。

--

散布図をTkinterウィンドウで表示するボタンをSAVE CSVの隣に作成することは可能ですか？

--

もちろん可能です。Tkinterウィンドウに散布図を表示するために、まずmatplotlibのFigureCanvasTkAggをインポートし、散布図を描画する関数を変更します。

--

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_scatter(phi_psi_data):
    fig, ax = plt.subplots()
    phi = [round(data[2], 2) for data in phi_psi_data]
    psi = [round(data[3], 2) for data in phi_psi_data]
    
    ax.scatter(phi, psi)
    ax.set_xlabel('Phi (degrees)')
    ax.set_ylabel('Psi (degrees)')
    ax.set_title('Phi-Psi Scatter Plot')

    return fig
    
--

次に、scatter_buttonを作成し、scatter_buttonが押されたときに散布図をTkinterウィンドウに表示する新しい関数show_scatterを作成します。

--

def show_scatter():
    phi_psi_data = extract_phi_psi(pdb_id, chain_id, structure)
    fig = plot_scatter(phi_psi_data)
    
    scatter_canvas = FigureCanvasTkAgg(fig, master=app)
    scatter_canvas.draw()
    scatter_canvas.get_tk_widget().grid(row=1, column=3, rowspan=2, padx=10, pady=10, sticky="nsew")

scatter_button = ttk.Button(app, text="Show Scatter Plot", command=show_scatter)
scatter_button.grid(row=2, column=2, padx=(0, 10), pady=10)

--

これで、Tkinterウィンドウに'Show Scatter Plot'ボタンが表示され、ボタンを押すと散布図が表示されるようになります。散布図は、PDB形式の出力とCSV形式でφとψの角度を表示するテキストボックスの右側に表示されます。

--

現在のコードは下記の通りです。SAVE CSVボタンが消えてしまいました。また、Show Scatter Plotボタンを押しても別のTkinterウィンドウに散布図が表示されません。何を修正すればよいでしょうか。

import sys
import csv
import math
import os
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder, protein_letters_3to1
from Bio.PDB.PDBExceptions import PDBConstructionWarning
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from io import StringIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_pdb(pdb_id):
    pdb_list = PDB.PDBList()
    filename = pdb_list.retrieve_pdb_file(pdb_id, pdir=".")
    return filename

    phi_psi_data = extract_phi_psi(pdb_id, chain_id, structure)
    write_to_csv(phi_psi_data, csv_output)
    
    csv_text.delete('1.0', tk.END)
    csv_output_str = csv_output.getvalue().replace('\r\n', '\n').replace('\r', '\n')
    csv_text.insert(tk.END, csv_output_str)
    
    plot_scatter(phi_psi_data)

def extract_phi_psi(pdb_id, chain_id, filename):
    file_format = os.path.splitext(filename)[1]
    if file_format == ".ent":
        parser = PDB.PDBParser(QUIET=True, PERMISSIVE=False)
    elif file_format == ".cif":
        parser = PDB.MMCIFParser(QUIET=True)
    else:
        raise ValueError("Invalid file format. Use either '.ent' (PDB) or '.cif' (mmCIF).")

    structure = parser.get_structure(pdb_id, filename)

    if chain_id not in [chain.id for chain in structure[0]]:
        raise ValueError(f"Chain {chain_id} not found in PDB structure.")

    ppb = PPBuilder()
    phi_psi = []

    for pp in ppb.build_peptides(structure[0][chain_id], aa_only=False):
        for residue, angles in zip(pp, pp.get_phi_psi_list()):
            res_name = residue.get_resname().upper()
            res_id = residue.get_id()[1]

            if res_name in PDB.Polypeptide.aa3:
                res_name_1 = protein_letters_3to1[res_name]
                phi, psi = angles

                if phi and psi:
                    phi_degrees = math.degrees(phi)
                    psi_degrees = math.degrees(psi)
                    phi_psi.append([res_name_1, res_id, phi_degrees, psi_degrees])

    return phi_psi

def write_to_csv(phi_psi_data, csv_output):
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])

    for residue_data in phi_psi_data:
        residue_name = residue_data[0]
        residue_id = residue_data[1]
        phi = round(residue_data[2], 2)  # 丸める
        psi = round(residue_data[3], 2)  # 丸める
        csv_writer.writerow([residue_name, residue_id, phi, psi])

def run_analysis():
    pdb_id = pdb_id_entry.get()
    chain_id = chain_id_entry.get()

    try:
        filename = fetch_pdb(pdb_id)
        phi_psi_data = extract_phi_psi(pdb_id, chain_id, filename)

        pdb_text.delete('1.0', tk.END)
        with open(filename, "r") as f:
            pdb_text.insert(tk.END, f.read())

        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

        csv_text.delete('1.0', tk.END)
        csv_output_str = csv_output.getvalue().replace('\r\n', '\n').replace('\r', '\n')
        csv_text.insert(tk.END, csv_output_str)

    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

def save_csv():
    pdb_id = pdb_id_entry.get()
    chain_id = chain_id_entry.get()
    default_filename = f"{pdb_id}_{chain_id}.csv"
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile=default_filename)
    if file_path:
        with open(file_path, "w") as f:
            f.write(csv_text.get("1.0", tk.END))

def plot_scatter(phi_psi_data):
    phi = [round(data[2], 2) for data in phi_psi_data]
    psi = [round(data[3], 2) for data in phi_psi_data]
    
    plt.scatter(phi, psi)
    plt.xlabel('Phi (degrees)')
    plt.ylabel('Psi (degrees)')
    plt.title('Phi-Psi Scatter Plot')
    plt.show()

def plot_scatter(phi_psi_data):
    fig, ax = plt.subplots()
    phi = [round(data[2], 2) for data in phi_psi_data]
    psi = [round(data[3], 2) for data in phi_psi_data]
    
    ax.scatter(phi, psi)
    ax.set_xlabel('Phi (degrees)')
    ax.set_ylabel('Psi (degrees)')
    ax.set_title('Phi-Psi Scatter Plot')

    return fig

def show_scatter():
    phi_psi_data = extract_phi_psi(pdb_id, chain_id, structure)
    fig = plot_scatter(phi_psi_data)
    
    scatter_canvas = FigureCanvasTkAgg(fig, master=app)
    scatter_canvas.draw()
    scatter_canvas.get_tk_widget().grid(row=1, column=3, rowspan=2, padx=10, pady=10, sticky="nsew")


app = tk.Tk()
app.title("PDB Phi-Psi Analyzer")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

pdb_id_label = ttk.Label(frame, text="PDB ID:")
pdb_id_label.grid(row=0, column=0, sticky=tk.W)
pdb_id_entry = ttk.Entry(frame, width=10)
pdb_id_entry.grid(row=0, column=1, sticky=tk.W)

chain_id_label = ttk.Label(frame, text="Chain ID:")
chain_id_label.grid(row=1, column=0, sticky=tk.W)
chain_id_entry = ttk.Entry(frame, width=10)
chain_id_entry.grid(row=1, column=1, sticky=tk.W)

analyze_button = ttk.Button(frame, text="Analyze", command=run_analysis)
analyze_button.grid(row=2, column=0, columnspan=2, pady=10)

pdb_text = tk.Text(app, wrap=tk.NONE, width=80, height=20)
pdb_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

pdb_scroll = ttk.Scrollbar(app, orient="vertical", command=pdb_text.yview)
pdb_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
pdb_text.config(yscrollcommand=pdb_scroll.set)

csv_text = tk.Text(app, wrap=tk.NONE, width=80, height=20)
csv_text.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))

csv_scroll = ttk.Scrollbar(app, orient="vertical", command=csv_text.yview)
csv_scroll.grid(row=1, column=3, sticky=(tk.N, tk.S))
csv_text.config(yscrollcommand=csv_scroll.set)

error_label = ttk.Label(app, text="", foreground="red")
error_label.grid(row=2, column=0, columnspan=2, pady=10)

save_button = ttk.Button(app, text="Save CSV", command=save_csv)
save_button.grid(row=2, column=2, pady=10)

scatter_button = ttk.Button(app, text="Show Scatter Plot", command=show_scatter)
scatter_button.grid(row=2, column=2, padx=(0, 10), pady=10)

app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=0)
app.columnconfigure(2, weight=1)
app.columnconfigure(3, weight=0)
app.rowconfigure(1, weight=1)

app.mainloop()

--

save_buttonが消えてしまっているのは、scatter_buttonを配置する際に同じグリッド位置で上書きされているためです。また、show_scatter関数でpdb_idとchain_idが定義されていないため、散布図が表示されません。これらの問題を修正しましょう。

以下の変更を行ってください。

scatter_buttonのgrid()メソッドでcolumnを3に変更してください。
show_scatter関数でpdb_idとchain_idを取得し、filenameをfetch_pdb()から取得します。
修正後のコードは以下のようになります。

--

# ...

# save_button のグリッドを修正
save_button.grid(row=2, column=1, pady=10)

# scatter_button のグリッドを修正
scatter_button.grid(row=2, column=3, padx=(0, 10), pady=10)

# ...

def show_scatter():
    pdb_id = pdb_id_entry.get()
    chain_id = chain_id_entry.get()
    filename = fetch_pdb(pdb_id)  # filename を取得

    phi_psi_data = extract_phi_psi(pdb_id, chain_id, filename)  # filename を渡す
    fig = plot_scatter(phi_psi_data)
    
    scatter_canvas = FigureCanvasTkAgg(fig, master=app)
    scatter_canvas.draw()
    scatter_canvas.get_tk_widget().grid(row=1, column=3, rowspan=2, padx=10, pady=10, sticky="nsew")

# ...

--

これで、SAVE CSVボタンが表示され、Show Scatter Plotボタンを押すと散布図が表示されるはずです。

--

def show_scatter():関数の位置はどこが良いでしょうか。

--

show_scatter()関数は他の関数と同じレベルで定義されているため、現在の位置でも問題ありません。ただし、関数の順序に一貫性を持たせるために、他の関連する関数（例えばrun_analysis()）の近くに移動させることができます。これは主にコードの可読性を向上させるための変更です。

以下のようにrun_analysis()の後にshow_scatter()を配置することができます。

--

# ...

def run_analysis():
    # run_analysis のコード

def show_scatter():
    # show_scatter のコード

def save_csv():
    # save_csv のコード

# ...

ただし、この変更はオプションであり、現在のshow_scatter()関数の位置でもコードは正常に機能します。関数の順序を変更するかどうかは、コードの整理と可読性に関連する個人的な選択です。

--

（個人的な選択！？ちがうChatGPTさんのスレッドだと違う感覚がでたりするのだろうか）

--

散布図のTkinterウィンドウをcsvを表示しているウィンドウと分けて別で表示したいです。何を変えればよいでしょうか。

--

散布図を別のTkinterウィンドウに表示するには、新しいトップレベルウィンドウを作成し、その中にFigureCanvasTkAggウィジェットを配置します。以下のようにshow_scatter()関数を変更してください：

--

def show_scatter():
    phi_psi_data = extract_phi_psi(pdb_id_entry.get(), chain_id_entry.get(), fetch_pdb(pdb_id_entry.get()))
    fig = plot_scatter(phi_psi_data)

    # 新しいトップレベルウィンドウを作成
    scatter_window = tk.Toplevel(app)
    scatter_window.title("Phi-Psi Scatter Plot")

    scatter_canvas = FigureCanvasTkAgg(fig, master=scatter_window)
    scatter_canvas.draw()
    scatter_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
--
この変更により、Show Scatter Plotボタンをクリックすると、新しいウィンドウが開き、その中に散布図が表示されます。

--

Phi-Psi Scatter Plotの最大値と最小値を180にしたいです。また、ヒートマップの上に散布図を表示することは可能でしょうか。

--


plot_scatter関数を変更して、Phi-Psi Scatter Plotのx軸とy軸の最大値と最小値を-180から180に設定できます。そして、ヒートマップを表示してその上に散布図を重ねることもできます。以下は、plot_scatter関数の変更例です。

--

import numpy as np
from scipy.stats import kde

def plot_scatter(phi_psi_data):
    fig, ax = plt.subplots()
    phi = [round(data[2], 2) for data in phi_psi_data]
    psi = [round(data[3], 2) for data in phi_psi_data]

    # ヒートマップ用のデータを計算
    x, y = np.array(phi), np.array(psi)
    nbins = 100
    k = kde.gaussian_kde([x, y])
    xi, yi = np.mgrid[-180:180:nbins * 1j, -180:180:nbins * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))

    # ヒートマップを描画
    im = ax.imshow(np.rot90(zi.reshape(xi.shape)), cmap=plt.cm.gist_earth_r,
                   extent=[-180, 180, -180, 180])

    # 散布図を描画
    ax.scatter(phi, psi, edgecolor='black', facecolor='none', alpha=0.7)

    # 軸の範囲を設定
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)

    ax.set_xlabel('Phi (degrees)')
    ax.set_ylabel('Psi (degrees)')
    ax.set_title('Phi-Psi Scatter Plot with Heatmap')

    return fig
    
--

この変更により、散布図の背景にヒートマップが表示され、x軸とy軸の範囲が-180から180に設定されます。

--

（3時間上限）

※180が表示されないのは間隔の問題、丸められていない、ヒートマップが表示できていない等の問題はあるが、聞き続けていたら解決してくれそうな気はする。今後に期待。

