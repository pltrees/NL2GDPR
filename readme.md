Extracting Page information using Coref:
1. First run /home/faysal-gpu/code/intern/gdpr-code-generator/src/coref/context_extractor.py
(it will read all the label data and extract the description. Then, it will store those description in a text files named by doc_index.)
2. Delete all the binary data from /home/faysal-gpu/code/intern/gdpr-code-generator/sota/coref_tool/conll-2012/data/. It sometimes creates problem if the folders are not empty when doing the post_process.
3. Run /home/faysal-gpu/code/intern/gdpr-code-generator/sota/coref_tool/process_data.py  (I used py36intern conda environment for this)
(it will process all the inputted text files and generate the corresponding pickle files for coref)
4. Execute /home/faysal-gpu/code/intern/gdpr-code-generator/sota/coref_tool/evaluate.py
5. Execute /home/faysal-gpu/code/intern/gdpr-code-generator/src/coref/postprocess_coref_cluster.py
(it will store all the coref information in /home/faysal-gpu/code/intern/gdpr-code-generator/src/coref/output/coref.json)

Extracting Feature Information using OIA:
1. Generate OIA graph for description using /home/faysal-gpu/code/intern/gdpr-code-generator/sota/oia_package/oia_package/diting/diting/parser/sentence2multi/as_graph/client.py
(it will store all the OIA graph in the following folder: /home/faysal-gpu/code/intern/gdpr-code-generator/sota/oia_package/oia_package/desc_ud/)
2. Execute /home/faysal-gpu/code/intern/gdpr-code-generator/src/FeatureDetector.py to extract all the features using OIA graph


Extracting UI information:
1. Run /home/faysal-gpu/code/intern/gdpr-code-generator/src/UIDetectory.py to collect all the UI element information


Policy Generator:
1. Generate OIA graph for purpose using /home/faysal-gpu/code/intern/gdpr-code-generator/sota/oia_package/oia_package/diting/diting/parser/sentence2multi/as_graph/client.py
2. To further improve the diversity using parapharse generator run /home/faysal-gpu/code/intern/gdpr-code-generator/src/PolicyGenerator.py.
(Detailed process on running paraphrase generator are given in /home/faysal-gpu/code/intern/gdpr-code-generator/src/Paraphrase/paraphraser-master/README.md)



