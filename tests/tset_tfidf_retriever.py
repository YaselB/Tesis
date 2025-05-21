def test_index_and_query(tmp_path):
    retr = TfidfRetriever(docs_path = "." , index_path= str(tem_path/"idx.pkl"))
    retr.texts = ["a b c" ,"a b d" ,"x y z"]
    retr.index()
    
    retr2 = TfidfRetriever(docs_path="." , index_path=str(tmp_path/"idx.pkl"))
    retr2.load_index()
    assert retr2.texts == retr.texts
    results = retr2.query("a b")
    # debería encontrar los dos primeros documentos (más parecidos)
    assert len(results) == 3
    # el más cercano debería ser el mismo texto
    assert result[0][1] <= results[1][1]
    