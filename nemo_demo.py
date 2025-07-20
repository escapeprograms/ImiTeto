import nemo.collections.asr as nemo_asr

asr_models = [model for model in dir(nemo_asr.models) if model.endswith("Model")]
print(asr_models)