import pytest


def test_save_load_result(example_json_resp, tmpdir):
    from i2vec_cli import models
    p = tmpdir.join("test.db").strpath
    sha256 = '4bd4c9a1eda6aee077168cef403769e0668bed610a41b9804e4d8f44867cc0a8'
    md5 = '1639d1f97128797ba2992a0c4be87f3d'
    prediction = example_json_resp['prediction']
    non_empty_prediction = {k: v for k, v in prediction.items() if v}
    models.database.init(p)
    models.init_all_tables()
    models.save_result(db=p, sha256=sha256, md5=md5, prediction=prediction)
    with pytest.raises(ValueError):
        models.load_result(db=p)
    load_res = models.load_result(db=p, sha256=sha256)
    assert load_res == non_empty_prediction
    load_res = models.load_result(db=p, md5=md5)
    assert load_res == non_empty_prediction
    load_res = models.load_result(db=p, sha256=sha256, md5=md5)
    assert load_res == non_empty_prediction


def test_load_result_from_empty_databse(tmpdir):
    from i2vec_cli import models
    p = tmpdir.join("test.db").strpath
    sha256 = '4bd4c9a1eda6aee077168cef403769e0668bed610a41b9804e4d8f44867cc0a8'
    md5 = '1639d1f97128797ba2992a0c4be87f3d'
    models.database.init(p)
    models.init_all_tables()
    with pytest.raises(models.Image.DoesNotExist):
        models.load_result(db=p, sha256=sha256)
    with pytest.raises(models.Image.DoesNotExist):
        models.load_result(db=p, md5=md5)
    with pytest.raises(models.Image.DoesNotExist):
        models.load_result(db=p, sha256=sha256, md5=md5)


def test_load_result_with_mismatch_checksum(tmpdir):
    from i2vec_cli import models
    p = tmpdir.join("test.db").strpath
    im1_sha256 = '4bd4c9a1eda6aee077168cef403769e0668bed610a41b9804e4d8f44867cc0a8'
    im1_md5 = '1639d1f97128797ba2992a0c4be87f3e'
    im2_sha256 = '4bd4c9a1eda6aee077168cef403769e0668bed610a41b9804e4d8f44867cc0a9'
    im2_md5 = '1639d1f97128797ba2992a0c4be87f3d'
    pred1 = {'group1': [('tag1', 0.1)]}
    pred2 = {'group2': [('tag2', 0.2)]}
    models.database.init(p)
    models.init_all_tables()
    models.save_result(db=p, sha256=im1_sha256, md5=im1_md5, prediction=pred1)
    models.save_result(db=p, sha256=im2_sha256, md5=im2_md5, prediction=pred2)
    with pytest.raises(ValueError):
        res = models.load_result(db=p, sha256=im1_sha256, md5=im2_md5)
