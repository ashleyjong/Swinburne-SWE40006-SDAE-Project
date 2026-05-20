dld@dld-Strix:~/Downloads/Year 3 Semester 2/SWE40006 Software Deployment and Evolution/Group Project/Work files$  source "/home/dld/Downloads/Year 3 Semester 2/SWE40006 Software Deployment and Evolution/Group Project/Work files/.venv/bin/activate"
(swinburne-swe40006-sdae-project) dld@dld-Strix:~/Downloads/Year 3 Semester 2/SWE40006 Software Deployment and Evolution/Group Project/Work files$ uv run pytest test_app.py -v
================================================================================================ test session starts =================================================================================================
platform linux -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- /home/dld/Downloads/Year 3 Semester 2/SWE40006 Software Deployment and Evolution/Group Project/Work files/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/dld/Downloads/Year 3 Semester 2/SWE40006 Software Deployment and Evolution/Group Project/Work files
configfile: pyproject.toml
plugins: anyio-4.13.0
collected 7 items                                                                                                                                                                                                    

test_app.py::test_frontend_serves PASSED                                                                                                                                                                       [ 14%]
test_app.py::test_read_empty_state PASSED                                                                                                                                                                      [ 28%]
test_app.py::test_write_and_llm_processing PASSED                                                                                                                                                              [ 42%]
test_app.py::test_write_invalid_payload PASSED                                                                                                                                                                 [ 57%]
test_app.py::test_delete_existing_item PASSED                                                                                                                                                                  [ 71%]
test_app.py::test_delete_non_existent_item PASSED                                                                                                                                                              [ 85%]
test_app.py::test_reset_data PASSED                                                                                                                                                                            [100%]

================================================================================================= 7 passed in 9.97s ==================================================================================================