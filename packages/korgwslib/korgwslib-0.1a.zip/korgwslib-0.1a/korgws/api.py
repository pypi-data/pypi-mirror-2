"""API classes for the korgws package."""

# korgws/api.py

__all__ = [
    'Library',
    'WSBank',
    'WSEffect',
    'WSObject',
    'WSPatch',
    'WSPerformance',
    'WSWaveSeq',
    'WSWaveStep',
    'WSWaveStepList',
]

from korgws.constants import *
from korgws.util import decode_name


class Library(object):
    pass

class WSBank(object):
    def __init__(self, name):
        self.name = name
        self.performances = []
        self.patches = []
        self.wave_seqs = []
        self.wave_steps = []

class WSObject(object):
    """Base class for Wavestation objects."""

    size_name = None

    def __init__(self, name=None, data=None):
        self._data = data
        if data:
            self._parse_data()
        if name:
            self.name = name

    def _parse_data(self):
        if self.size_name:
            self.name = decode_name(self._data[:self.size_name])


class WSEffect(WSObject):
    pass


class WSPerformance(WSObject):
    """Performance Data Structure

    typedef struct
    {
        char Perf_Name[NAME_SIZE]	;	/* Performance name - up to 16 
                characters */
        byte Fx_Perf_Block[21];		/* Leave space for effects 
                parameters */
        part Parts[8]; 				/* This is where the PART 
                blocks start, of which 8 can be 
                appended to the performance */
    } performance;

    typedef struct
    {
        byte  Bank_Num;   /* Bank number this PART is playing */
        byte  Patch_Num;  /* Patch number this PART is playing */
        ubyte Level;      /* Volume for this part */
        byte  0utput;     /* OUTPUT CHAN FOR THIS Part (-1 = stereo) */
        ubyte Part_Mode;  /* KEYBOARD ASSIGN MODE (Polyphonic,UNI) */
                          /* bit 6 */
                          /* 1 = Patch is from Expansion RAM Bank (RAM3) */
                          /* bit 5-4 */
                          /* 00 = **** */
                          /* 01 = Local play mode*/
                          /* 10 = MIDI play mode*/
                          /* 11 = Both */
                          /* bit 3-2 */
                          /* 00 = **** */
                          /* 01 = polyphonic*/
                          /* 10 = unison re-trigger*/
                          /* 11 = unison legato*/
                          /* bit 1-0 */
                          /* 00 = low note*/
                          /* 01 = high note*/
                          /* 10 = last note*/
                          /* 11 = **** */

        ubyte Lo_Key;       /* Lower note of keyboard range*/
        ubyte Hi_Key;       /* Upper note of keyboard range*/
        ubyte Lo_Vel;       /* Lower limit of velocity range*/
        ubyte Hi_Vel;       /* Upper limit of velocity range */
        byte  Trans;        /* Transpose value in semitones */
        byte  Detune;       /* Detune value in cents*/
        ubyte Tunetab;      /* Micro tuning table for this PART */
        ubyte Micro_Tune_Key; /* Root key for pure major/minor and USER scales */
        ubyte Midi_Out_Chan;  /* MIDI transmit channel for this PART */
        byte  Midi_Prog_Num;  /* MIDI prog# to xmit when PART selected, -1=off */
        byte  Sus_Enable;     /* Sustain Pedal enable/disable */
        uword Delay;          /* Delay value in milliseconds */
    } part;
    
    """
    size_name = SIZE_PERF_NAME


class WSPatch(WSObject):
    """Patch Data Structure

    /*        Individual Patch Data Structure */
    /* This is the structure for data that is individual to the */
    /* 1, 2, or 4 oscillators that make up a Patch.*/
    /* Four of these structures are included in a Patch.*/

    typedef struct
    {
        byte	Wave_Coarse;	/* Wave detuning in semitones */
        byte	Wave_Fine;		/* Wave detuning in cents */
        ubyte	Wave_Bank;		/* Wave bank */
        uword	Wave_Num;		/* Wave number*/
        byte	Wave_Scale;		/* Wave pitch scaling slope */
        ubyte	Lfo1_Rate;		/* LFO 1 Rate */
        ubyte	Lfo1_Amt;		/* LFO 1 Amount */
        ubyte	Lfo1_Delay;		/* LFO 1 Delay */
        ubyte	Lfo1_Fade;		/* LFO 1 Fade in */
        ubyte	Lfo1_Shape;		/* LFO 1 Shape (bits 0-6) 1-127 */
                                /* LFO 1 Sync (bit 7) */
                                /* 1 = Sync on */
                                /* 0 = Sync off */
        byte	S1_Lfo1_R;		/* Mod Source to LFO 1 Rate pointer */
        byte	S1_Lfo1_R_Amt; 	/* Mod Source to LFO 1 Rate amount */
        byte	S1_Lfo1_A;		/* Mod Source to LFO 1 Amt pointer */
        byte	S1_Lfo1_A_Amt;	/* Mod Source to LFO 1 Amt amount */
        ubyte	Lfo2_Rate;		/* LFO 2 Rate */
        ubyte	Lfo2_Amt;		/* LFO 2 Amount */
        ubyte	Lfo2_Delay;		/* LFO 2-Delay */
        ubyte	Lfo2_Fade;		/* LFO 2-Fade in */
        ubyte	Lfo2_Shape;		/* LFO 2-Shape (bits 0-6) 1-127 */
                                /* LFO 2 Sync (bit 7) */
                                /* 1 = Sync on */
                                /* 0 = Sync off */
        byte	S1_Lfo2_R;		/* Mod Source to LFO 1 Rate pointer */
        byte	S1_Lfo2_R Amt;	/* Mod Source to LFO 2 Rate amount */
        byte	S1_Lfo2_A;		/* Mod Source to LF0 2 Amt pointer */
        byte	S1_Lfo2_A Amt;	/* Mod Source to LFO 1 Amt amount */
        ubyte	EG_Rate1;		/* Envelope 1 Rate 1 */
        ubyte	EG_Rate2;		/* Envelope 1 Rate 2 */
        ubyte	EG_Rate3;		/* Envelope 1 Rate 3 */
        ubyte	EG_Rate4;		/* Envelope 1 Rate 4 */
        ubyte	EG_Level0;		/* Envelope 1 Level 0 */
        ubyte	EG_Level1;		/* Envelope 1 Level 1 */
        ubyte	EG_Level2;		/* Envelope 1 Level 2 */
        ubyte	EG_Level3;		/* Envelope 1 Level 3 */
        ubyte	EG_Level4;		/* Envelope 1 Level 4 */
        byte	Vel_EG_A;		/* Velocity to Env1 Amount Amt */
        ubyte	AEG_Rate1;		/* Amplitude Envelope Rate 1 */
        ubyte	AEG_Rate2;		/* Amplitude Envelope Rate 2 */
        ubyte	AEG_Rate3;		/* Amplitude Envelope Rate 3 */
        ubyte	AEG_Rate4;		/* Amplitude Envelope Rate 4 */
        ubyte	AEG_Level0;		/* Amplitude Envelope Level 0 */
        ubyte	AEG_Level1;		/* Amplitude Envelope Level 1 */
        ubyte	AEG_Level2;		/* Amplitude Envelope Level 2 */
        ubyte	AEG_Level3;		/* Amplitude Envelope Level 3 */
        byte	Pitch_Mac;		/* Pitch Macro number */
        byte	Fil_Mac;		/* Filter Macro number */
        byte	Amp_Mac;		/* Amplitude Envelope Macro number */
        byte	Pan_Mac;		/* Pan Macro number */
        byte	Env_Mac;		/* Envelope 1 macro number */
        byte	Pw_Range;		/* Pitchwheel Range */
        byte	S1_Pitch;		/* Modulation Source 1 to Pitch pointer */
        byte	S1_Pitch_Amt;	/* Modulation Source 1 to Pitch Amount*/
        byte	S2_Pitch;		/* Modulation Source 2 to Pitch pointer */
        byte	S2_Pitch_Amt;	/* Modulation Source 2 to Pitch Amount */
        byte	Key_Filter;     /* Keyboard to Filter Cutoff Amount */
        byte	S1_Filter;	    /* Modulation Source 1 to Filter pointer */
        byte	S1_Filter_Amt;	/* Modulation Source 1 to Filter Amount */
        byte	S2_Filter;		/* Modulation Source 2 to Filter pointer */
        byte	S2_Filter_Amt;	/* Modulation Source 2 to Filter Amount */
        byte	Vel_AEG_A;		/* Velocity to Amp Env Amount Amount */
        byte	Vel_AEG_R;		/* Velocity To Amp Env Attack Rate Amt */
        byte	Key AEG_R;		/* Keyboard to Amp Env Decay Rate Amt */
        byte	S1_Amp;			/* Modulation Source 1 to Amp pointer */
        byte	S1_Amp_Amt;		/* Modulation Source 1 to Amp Amount */
        byte	S2_Amp;			/* Modulation Source 2 to Amp pointer */
        byte	S2_Amp_Amt;		/* Modulation Source 2 to Amp Amount */
        byte	Key_Pan_Amt;	/* Keyboard to Pan Amount */
        byte	Vel_Pan_Amt;	/* Velocity to Pan Amount */
        ubyte	Cutoff;			/* Filter Cutoff value */
        ubyte	Filter_Exciter;	/* Filter Exciter value */
        byte	Vel_EG_R;		/* Velocity to ENV1 rate amount */
        byte	Key_EG_R;		/* Keyboard to ENV1 rate amount */
        byte	PEG_Amt;		/* Pitch Ramp amount */
        ubyte	PEG_Rate;		/* Pitch Ramp rate */
        byte	Vel_PEG_A;		/* Velocity to pitch ramp amount */
        byte	Indiv_Level;	/* Velocity to pitch ramp rate amount */
        long	Lfo1_Inc;		/* Lfo fade in amount increment */
        long	Lfo2_Inc;		/* Lfo fade in amount increment */
        byte	Patch_Output;	/* Individual output routing */
        byte	Wave_Num_Exp;	/* Wave number expansion to access
                                   Expansion PCM data (Waves numbered 
                                   397 and over). This number is added 
                                   to the value of Wave_Num to determine
                                   the actual wave number.*/
    } indiv;

    /*	Patch data structure	*/

    typedef struct
    {
        char	Patch Name[16];	/* Patch name up to 16 characters*/
        ubyte	Mix_Rate1;		/* Mix envelope rate for segment 1 */ 
        ubyte	Mix_Rate2; 		/* Mix envelope rate for segment 2 */ 
        ubyte	Mix_Rate3; 		/* Mix envelope rate for segment 3 */ 
        ubyte	Mix_Rate4; 		/* Mix envelope rate for segment 4 */ 
        uword	Mix_Count1; 	/* Number of update cycles for env seg*/ 
        uword	Mix_Count2; 	/* Number of update cycles for env seg*/ 
        uword	Mix_Count3; 	/* Number of update cycles for env seg*/ 
        uword	Mix_Count3B;	/* Number of update cycles for env seg*/ 
        uword	Mix_Count2B;	/* Number of update cycles for env seg*/ 
        uword	Mix_Count1B;	/* Number of update cycles for env seg*/ 
        uword	Mix_Count4; 	/* Number of update cycles for env seg*/
        long	Mix_XSlope1;	/* Increment size for env seg 1 */ 
        long	Mix_XSlope2;	/* Increment size for env seg 2 */ 
        long	Mix_XSlope3;	/* Increment size for env seg 3 */
        long	Mix_XSlope4;	/* Increment size for env seg 4 */
        long	Mix_YSlope1;	/* Increment size for env seg 1 */
        long	Mix_YSlope2;	/* Increment size for env seg 2 */
        long	Mix_YSlope3;	/* Increment size for env seg 3 */ 
        long	Mix_YSlope4;	/* Increment size for env seg 4 */
        ubyte	Mix_X0;		    /* Mix Envelope Point 0 level */
        ubyte	Mix_X1;			/* Mix Envelope Point 1 level */
        ubyte	Mix_X2;			/* Mix Envelope Point 2 level */
        ubyte	Mix_X3;			/* Mix Envelope Point 3 level */
        ubyte	Mix_X4;			/* Mix Envelope Point 4 level */
        ubyte	Mix_Y0;			/* Mix Envelope Point 0 level */
        ubyte 	Mix_Y1;			/* Mix Envelope Point 1 level */
        ubyte	Mix_Y2;			/* Mix Envelope Point 2 level */
        ubyte	Mix_Y3;			/* Mix Envelope Point 3 level */
        ubyte	Mix_Y4;			/* Mix Envelope Point 4 level */
        ubyte	Mix_Repeats;	/* Number of repeats of mix envelope*/
        ubyte	Mix_Env_Loop;	/* Start segment of Mix Envelope loops*/
        ubyte	S1_MixAC;		/* Modulation Source 1 to MixAC pointer*/
        byte	S1_MixAC_Amt;	/* Modulation Source 1 to MixAC Amount*/
        ubyte	S2_MixAC; 		/* Modulation Source 2 to MixAC pointer*/
        byte	S2_MixAC_Amt;	/* Modulation Source 2 to MixAC Amount*/
        ubyte	S1_MixBD; 		/* Modulation Source 1 to MixBD pointer*/
        byte	S1_MixBD_Amt;	/* Modulation Source 1 to MixBD Amount*/
        ubyte	S2_MixBD; 		/* Modulation Source 2 to MixBD pointer*/
        byte	S2_MixBD_Amt;	/* Modulation Source 2 to MixBD Amount*/
        byte	Number_Of_Waves;/* Number of WAVES/WAVESEQS in Patch*/
        ubyte	Hard_Sync; 		/* Hard Sync Flag*/
        byte	Bank_Exp; 		/* Bit 3 = 1; Wave D uses RAM3 waveseq */ 
                                /* Bit 2 = 1; Wave C uses RAM3 waveseq */ 
                                /* Bit 1 = 1; Wave B uses RAM3 waveseq */ 
                                /* Bit 0 = 1; Wave A uses RAM3 waveseq */ 
        byte	Dummy141; 		/* Extra for future use */
        indiv 	waveA;			/* Individual parameters for WAVE A */
        indiv 	waveB;			/* Individual parameters for WAVE B */
        indiv 	waveC;			/* Individual parameters for WAVE C */
        indiv 	waveD;			/* Individual parameters for WAVE D */
    } patch;
    
    """
    size_name = SIZE_PATCH_NAME


class WSWaveSeq(WSObject):
    """Wave Sequence Data Structure.

    typedef struct {
        uword WS_Link;        /* Pointer to Wave Sequence Start Step */
        uword WS_Slink;       /* Pointer to Startmod Start Step */
        ubyte WS_Loop_Start;  /* Step number of WAVESEQ Loop Start Point step */
        ubyte WS_Loop_End;    /* Step number of WAVESEQ Loop End Point step */
        ubyte WS_Loop_Count;  /* - Loop repeat count (bits 0-6) 1-127 */
                              /* O = OFF     */
                              /* 127 = 1NF */
                              /* Loop Direction (bit 7) */
                              /* O = FOR */
                              /* 1 = B/F */
        ubyte WS_Start_Step,  /* Startmod starting step number*/
        ubyte WS_Mod_Src;     /* Controller number to use for startmod */
        byte  WS_Mod_Amt;     /* Startmod sensitivity */
        word  WS_Dyno_Mod;    /* (Total_Time * Mod_Amt) / 255 */
        uword WS_Start_Time;  /* Cumulative time up to start step */
        uword WS_Time;        /* Total time of Wave Sequence */
    } waveseq;

    """

    size_name = SIZE_WAVESEQ_NAME


class WSWaveStep(WSObject):
    """Data structure of each STEP in a WAVE SEQUENCE.

    typedef struct {
        uword WS_Flink;     /* Step number of step in WAVSEQ after this one */
        uword WS_Blink;     /* Step number of step in WAVSEQ before this one */
        uword WS_Llink;     /* Pointer to loop start (0xFFFF except last step) */
        uword WS_Wave_Num;  /* Wave number of this step in wave sequence */
        byte  WS_Coarse;    /* -24 to 24: Coarse tuning of wave */
                            /* 25 to 47: illegal values
                               48 to 96: subtract 72 for actual coarse tuning
                               and use expanded PCM, adding 365 to WS_Wave_Num
                               value for actual PCM wave number. */
        byte  WS_Fine;		/* Fine tuning of wave */
        uword WS_Xfade;		/* Crossfade time of wave */
        uword WS_Duration;	/* Duration of wave */
        ubyte WS_Level;		/* Level of wave */
        ubyte WS_Mod_Index;	/* Modulation Index */
    } wavestep;
    
    """

class WSWaveStepList(list):
    """A list container for all WaveSteps in a bank."""
    pass
