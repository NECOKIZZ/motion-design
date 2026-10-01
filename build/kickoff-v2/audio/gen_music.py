# Generate ~44s of music with MusicGen: a 30s seed, then a continuation conditioned on the seed's tail.
import sys, numpy as np, torch, soundfile as sf
from transformers import AutoProcessor, MusicgenForConditionalGeneration
model_id, prompt, out, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
torch.manual_seed(seed); torch.set_num_threads(4)
proc = AutoProcessor.from_pretrained(model_id); model = MusicgenForConditionalGeneration.from_pretrained(model_id)
sr = model.config.audio_encoder.sampling_rate
inp = proc(text=[prompt], padding=True, return_tensors="pt")
a = model.generate(**inp, do_sample=True, guidance_scale=3.5, max_new_tokens=int(30*50))[0,0].numpy()
print("seed", a.shape[0]/sr, flush=True)
tail = a[-int(10*sr):]
inp2 = proc(audio=tail, sampling_rate=sr, text=[prompt], padding=True, return_tensors="pt")
b = model.generate(**inp2, do_sample=True, guidance_scale=3.5, max_new_tokens=int(25*50))[0,0].numpy()
# b contains the 10s prompt + 15s new; append only new part
new = b[len(tail):] if b.shape[0] > len(tail) else b
y = np.concatenate([a, new])
sf.write(out, y, sr); print("wrote", out, y.shape[0]/sr, flush=True)
