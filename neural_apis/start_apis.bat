cd ./nlp_api

uvicorn nlp_api:nlp_app --host 0.0.0.0 --port 8400
uvicorn translator_api:translator_app --host 0.0.0.0 --port 8900
cd ../stable_diff_api
uvicorn stable_diff_api:stable_diff_app --host 0.0.0.0 --port 8500
cd ../video_description_api
uvicorn video_description_api:video_description_app --host 0.0.0.0 --port 8600
cd ../upscale_api
uvicorn ups.caler_api:upscaler_app --host 0.0.0.0 --port 8300

cd ../../use_cases
uvicorn use_cases_api:use_cases_app --host 0.0.0.0 --port 8000