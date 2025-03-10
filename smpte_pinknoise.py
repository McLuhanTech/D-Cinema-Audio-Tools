
// Band-Limited Pink Noise Generator
// Produces band limited, pink noise from pseudorandom numbers
// Inputs:
// int SampleRate
// int Period
//

// float HpFc
// float LpFc
// float MaxPeak
// Revised 2015-01-04 by Calvert Dayton

 float maxAmp = 10.0^(MaxPeak / 20.0);
 float pi = 3.141592654;

 // Initialize variables for generating a random number
 int randMax = Period - 1;
 int seed = 0;
 float white = 0.0;
 float scaleFactor = 2.0 / float(randMax);
 int randStep = 52737;
 // 1024k Samples at 9600 or 88200 sample rate is a special case
 if (Period == 1048576 and SampleRate > 48000) { randStep = 163841 };

 // Calculate omegaT for matched Z transform highpass filters
 float w0t = 2.0 * pi * HpFc / float(SampleRate);

 // Disaster check: Limit LpFc <= Nyquist
 if (LpFc > float(SampleRate / 2.0) { LpFc = float(SampleRate / 2.0) };

 // Calculate k for bilinear transform lowpass filters
 float k = tan(( 2.0 * pi * LpFc / float(SampleRate)) / 2.0);
 float k2 = k * k;

 // Calculate biquad coefficients for bandpass filter components
 hp1_a1 = -2.0 * exp(-0.3826835 * w0t) * cos(0.9238795 * w0t);
 hp1_a2 = exp(2.0 * -0.3826835 * w0t);
 hp1_b0 = (1.0 - hp1_a1 + hp1_a2) / 4.0;
 hp1_b1 = -2.0 * hp1_b0;
 hp1_b2 = hp1_b0;
 hp2_a1 = -2.0 * exp(-0.9238795 * w0t) * cos(0.3826835 * w0t);
 hp2_a2 = exp(2.0 * -0.9238795 * w0t);
 hp2_b0 = (1.0 - hp2_a1 + hp2_a2) / 4.0;
 hp2_b1 = -2.0 * hp2_b0;
 hp2_b2 = hp2_b0;

 lp1_a1 = (2.0 * (k2 - 1.0)) / (k2 + (k / 1.306563) + 1.0);
 lp1_a2 = (k2 - (k / 1.306563) + 1.0) / (k2 + (k / 1.306563) + 1.0);
 lp1_b0 = k2 / (k2 + (k / 1.306563) + 1.0);
 lp1_b1 = 2.0 * lp1_b0;
 lp1_b2 = lp1_b0;

 lp2_a1 = (2.0 * (k2 - 1.0)) / (k2 + (k / 0.541196) + 1.0);
 lp2_a2 = (k2 - (k / 0.541196) + 1.0) / (k2 + (k / 0.541196) + 1.0);
 lp2_b0 = k2 / (k2 + (k / 0.541196) + 1.0);
 lp2_b1 = 2.0 * lp2_b0;
 lp2_b2 = lp2_b0;

 // Initialize delay line variables for bandpass filter
 float w = 0.0;
 float hp1w1 = 0.0;
 float hp1w2 = 0.0;
 float hp2w1 = 0.0;
 float hp2w2 = 0.0;
 float lp1w1 = 0.0;
 float lp1w2 = 0.0;
 float lp2w1 = 0.0;
 float lp2w2 = 0.0;

 // Initialize delay lines for pink filter network
 float pink = 0.0;
 float lp1 = 0.0;
 float lp2 = 0.0;
 float lp3 = 0.0;
 float lp4 = 0.0;
 float lp5 = 0.0;
 float lp6 = 0.0;

 // For each iteration of the noise generator

 // Generate a pseudorandom number using linear congruential PRNG (LCG).
 // Bitwise AND with randMax forces sign bit positive and zeroes any unwanted bits.
 seed = (1664525 * seed + randStep) & randMax;
 // Scale to a real number in the range -1.0 <= white <= 1.0
 white = float(seed) * scaleFactor - 1.0;

 // Run pink filter; a parallel network of first-order LP filters, scaled to
 // produce an output signal with target RMS = -21.5 dB FS (-18.5 dB AES FS)
 // when bandpass filter cutoff frequencies are 10 Hz and 22.4 kHz.
 lp1 = 0.9994551 * lp1 + 0.00198166688621989 * white;
 lp2 = 0.9969859 * lp2 + 0.00263702334184061 * white;
 lp3 = 0.9844470 * lp3 + 0.00643213710202331 * white;
 lp4 = 0.9161757 * lp4 + 0.01438952538362820 * white;
 lp5 = 0.6563399 * lp5 + 0.02698408541064610 * white;
 pink = lp1 + lp2 + lp3 + lp4 + lp5 + lp6 + white * 0.0342675832159306;
 lp6 = white * 0.0088766118009356;

 // Run bandpass filter; a series network of 4 biquad filters
 // Biquad filters implemented in Direct Form II
 w = pink - hp1_a1 * hp1w1 - hp1_a2 * hp1w2;
 pink = hp1_b0 * w + hp1_b1 * hp1w1 + hp1_b2 * hp1w2;
 hp1w2 = hp1w1;
 hp1w1 = w;

 w = pink - hp2_a1 * hp2w1 - hp2_a2 * hp2w2;
 pink = hp2_b0 * w + hp2_b1 * hp2w1 + hp2_b2 * hp2w2;
 hp2w2 = hp2w1;
 hp2w1 = w;

 w = pink - lp1_a1 * lp1w1 - lp1_a2 * lp1w2;
 pink = lp1_b0 * w + lp1_b1 * lp1w1 + lp1_b2 * lp1w2;
 lp1w2 = lp1w1;
 lp1w1 = w;

 w = pink - lp2_a1 * lp2w1 - lp2_a2 * lp2w2;
 pink = lp2_b0 * w + lp2_b1 * lp2w1 + lp2_b2 * lp2w2;
 lp2w2 = lp2w1;
 lp2w1 = w;

 // Limit peaks to ± MaxAmp
 if (pink > MaxAmp) {pink = MaxAmp};
 if (pink < -MaxAmp) {pink = -MaxAmp};
 // Do something with the output sample stored in "pink" before repeating