def test_dimensions():
    feats = extract_features("datasets/sample_full.jpg", resize=False)
    assert feats["width"] == 512 and feats["height"] == 384
