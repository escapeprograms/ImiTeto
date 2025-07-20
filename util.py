import numpy as np
from scipy.fft import fft

def spectral_flatness(audio_chunk, threshold=0.5):
    """
    Determines if an audio chunk contains speech by calculating its spectral flatness.
    
    Args:
        audio_chunk (np.ndarray): A 1D numpy array of audio data (float32).
        threshold (float): The flatness cutoff. Lower values indicate speech.
        
    Returns:
        bool: True if the chunk is likely speech, False otherwise.
    """
    # Calculate the power spectrum using the Fast Fourier Transform
    N = len(audio_chunk)
    if N == 0:
        return False
        
    magnitudes = np.abs(fft(audio_chunk))[:N//2]
    power_spectrum = magnitudes**2
    
    # Ensure no zero values to avoid errors in geometric mean calculation
    power_spectrum[power_spectrum == 0] = 1e-10

    # Calculate the geometric mean and arithmetic mean
    geometric_mean = np.exp(np.mean(np.log(power_spectrum)))
    arithmetic_mean = np.mean(power_spectrum)

    # Calculate spectral flatness
    spectral_flatness = geometric_mean / arithmetic_mean
    
    # Compare to the threshold
    # A low flatness value (peaky spectrum) indicates speech
    return spectral_flatness



def spectral_flux(audio_chunk, prev_spec, threshold=1000):
    """
    Determines if an audio chunk contains speech by calculating spectral flux.
    
    Returns:
        A tuple: (is_speech, current_spectrum)
    """
    global previous_spectrum # Or pass it as an argument
    
    # Calculate the magnitude spectrum of the current chunk
    N = len(audio_chunk)
    if N == 0:
        return False, np.array([])
        
    current_spectrum = np.abs(fft(audio_chunk))[:N//2]
    
    # On the first run, just store the spectrum and assume silence
    if prev_spec is None:
        return False, current_spectrum

    # Calculate the spectral flux (sum of squared differences)
    flux = np.sqrt(np.sum((current_spectrum - prev_spec) ** 2)) / N
    
    return flux, current_spectrum