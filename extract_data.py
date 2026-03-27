import zipfile
import xml.etree.ElementTree as ET
import os
import json

def extract_docx_data(docx_path, output_dir):
    data = []
    if not os.path.exists(docx_path):
        print(f"File {docx_path} not found.")
        return data

    with zipfile.ZipFile(docx_path, 'r') as docx:
        # Get relationships to map Rid to image path
        rels_xml = docx.read('word/_rels/document.xml.rels')
        rels_root = ET.fromstring(rels_xml)
        rels = {}
        ns_rels = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
        for rel in rels_root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
            rels[rel.get('Id')] = rel.get('Target')

        # Get the main document content
        doc_xml = docx.read('word/document.xml')
        doc_root = ET.fromstring(doc_xml)
        
        # OpenXML namespaces
        ns = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
            'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture'
        }

        # Find all paragraphs
        paragraphs = doc_root.findall('.//w:p', ns)
        current_item = None
        
        for p in paragraphs:
            # Check for images in this paragraph
            drawings = p.findall('.//w:drawing', ns)
            if drawings:
                for drawing in drawings:
                    blips = drawing.findall('.//a:blip', ns)
                    for blip in blips:
                        rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if rid in rels:
                            image_path = rels[rid]
                            # image_path is like 'media/image1.png'
                            filename = os.path.basename(image_path)
                            current_item = {"image": filename, "mnemonic": ""}
                            data.append(current_item)
            
            # Check for text in this paragraph
            texts = p.findall('.//w:t', ns)
            if texts and current_item:
                mnemonic_part = "".join([t.text for t in texts if t.text])
                if mnemonic_part.strip():
                    if current_item["mnemonic"]:
                        current_item["mnemonic"] += "\n" + mnemonic_part
                    else:
                        current_item["mnemonic"] = mnemonic_part

    return data

hiragana_data = extract_docx_data('📘 HIRAGANA.docx', 'assets/hiragana')
katakana_data = extract_docx_data('📘 KATAKANA.docx', 'assets/katakana')

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump({
        "hiragana": hiragana_data,
        "katakana": katakana_data
    }, f, ensure_ascii=False, indent=2)

print("Data extracted successfully to data.json")
