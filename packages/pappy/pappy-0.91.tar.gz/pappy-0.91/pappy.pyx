from time import sleep

cdef extern from "Python.h":
	object PyCObject_FromVoidPtr( void* cobj, void (*destr)(void *))
	void *PyCObject_AsVoidPtr(object)
	void PyEval_InitThreads()
	ctypedef int PyGILState_STATE
	PyGILState_STATE PyGILState_Ensure()
	void PyGILState_Release(PyGILState_STATE gstate)
	
cdef extern from "portaudio.h":

	# Retrieve the release number of the currently running PortAudio build,
	# eg 1900.
	#
	# int Pa_GetVersion( void );
	int Pa_GetVersion()

	# Retrieve a textual description of the current PortAudio build,
	# eq "PortAudio V19-devel 13 October 2002"
	#
	char *Pa_GetVersionText()

	# Error codes returned by PortAudio functions.
	# Note that with the exception of paNoError, all PaErrorCodes are negative.
	#
	ctypedef int PaError
	ctypedef enum PaErrorCode:
		paNoError = 0
		paNotInitialized = -10000
		paUnanticipatedHostError
		paInvalidChannelCount
		paInvalidSampleRate
		paInvalidDevice
		paInvalidFlag
		paSampleFormatNotSupported
		paBadIODeviceCombination
		paInsufficientMemory
		paBufferTooBig
		paBufferTooSmall
		paNullCallback
		paBadStreamPtr
		paTimedOut
		paInternalError
		paDeviceUnavailable
		paIncompatibleHostApiSpecificStreamInfo
		paStreamIsStopped
		paStreamIsNotStopped
		paInputOverflowed
		paOutputUnderflowed
		paHostApiNotFound
		paInvalidHostApi
		paCanNotReadFromACallbackStream
		paCanNotWriteToACallbackStream
		paCanNotReadFromAnOutputOnlyStream
		paCanNotWriteToAnInputOnlyStream
		paIncompatibleStreamHostApi
		paBadBufferPtr

	# Translate the supplied PortAudio error code into a human readable
	# message.
	#
	char *Pa_GetErrorText(PaError errorCode)
	
	# Library initialization function - call this before using PortAudio.
	# This function initialises internal data structures and prepares 
	# underlying host APIs for use.  With the exception of Pa_GetVersion(),
	# Pa_GetVersionText(), and Pa_GetErrorText(), this function MUST be called
	# before using any other PortAudio API functions.
	#
	# If Pa_Initialize() is called multiple times, each successful
	# call must be matched with a corresponding call to Pa_Terminate().
	# Pairs of calls to Pa_Initialize()/Pa_Terminate() may overlap, and are 
	# not required to be fully nested.
	#
	# Note that if Pa_Initialize() returns an error code, Pa_Terminate()
	# should NOT be called.
	#
	# @return paNoError if successful, otherwise an error code indicating the
	# cause of failure.
	#
	# @see Pa_Terminate
	#
	PaError Pa_Initialize()

	# Library termination function - call this when finished using PortAudio.
	# This function deallocates all resources allocated by PortAudio since it 
	# was initializied by a call to Pa_Initialize(). In cases where 
	# Pa_Initialize() has been called multiple times, each call must be 
	# matched with a corresponding call to Pa_Terminate(). The final matching 
	# call to Pa_Terminate() will automatically close any PortAudio streams 
	# that are still open.
	#
	# Pa_Terminate() MUST be called before exiting a program which uses 
	# PortAudio. Failure to do so may result in serious resource leaks, such 
	# as audio devices not being available until the next reboot.
	#
	# @return paNoError if successful, otherwise an error code indicating the 
	# cause of failure.
	#
	# @see Pa_Initialize
	# 
	PaError Pa_Terminate()
	
	# The type used to refer to audio devices. Values of this type usually
	# range from 0 to (Pa_GetDeviceCount()-1), and may also take on the 
	# PaNoDevice and paUseHostApiSpecificDeviceSpecification values.
	#
	# @see Pa_GetDeviceCount, paNoDevice, 
	# 	paUseHostApiSpecificDeviceSpecification
	# 
	ctypedef int PaDeviceIndex
	
	cdef PaDeviceIndex paNoDevice
	cdef PaDeviceIndex paUseHostApiSpecificDeviceSpecification
#
# Host API enumeration mechanism
#

	# The type used to enumerate to host APIs at runtime. Values of this type
	# range from 0 to (Pa_GetHostApiCount()-1).
	#
	# @see Pa_GetHostApiCount
	# 
	ctypedef int PaHostApiIndex

	# Retrieve the number of available host APIs. Even if a host API is
	# available it may have no devices available.
	#
	# @return A non-negative value indicating the number of available host APIs
	# or, a PaErrorCode (which are always negative) if PortAudio is not initialized
	# or an error is encountered.
	#
	# @see PaHostApiIndex
	# 
	PaHostApiIndex Pa_GetHostApiCount()

	# Retrieve the index of the default host API. The default host API will be
	# the lowest common denominator host API on the current platform and is
	# unlikely to provide the best performance.
	#
	# @return A non-negative value ranging from 0 to (Pa_GetHostApiCount()-1)
	# indicating the default host API index or, a PaErrorCode (which are always
	# negative) if PortAudio is not initialized or an error is encountered.
	# 
	PaHostApiIndex Pa_GetDefaultHostApi()

	# Unchanging unique identifiers for each supported host API. This type
	# is used in the PaHostApiInfo structure. The values are guaranteed to be
	# unique and to never change, thus allowing code to be written that
	# conditionally uses host API specific extensions.
	#
	# New type ids will be allocated when support for a host API reaches
	# "public alpha" status, prior to that developers should use the
	# paInDevelopment type id.
	#
	# @see PaHostApiInfo
	# 
	ctypedef enum PaHostApiTypeId:
		paInDevelopment=0	# use while developing support for a new host API
		paDirectSound=1
		paMME=2
		paASIO=3
		paSoundManager=4
		paCoreAudio=5
		paOSS=7
		paALSA=8
		paAL=9
		paBeOS=10
		paWDMKS=11
		paJACK=12
		paWASAPI=13
		paAudioScienceHPI=14

	# A structure containing information about a particular host API. 
	#
	ctypedef struct PaHostApiInfo:
		int structVersion					# struct version
		PaHostApiTypeId type				# well-known unique identifier of
											# 	this host API
		char *name							# textual description of host APIs
											#   for display on UIs
		int deviceCount						# number of devices belonging to
											#   this host API. This field may
											#	be used in conjunction with 
											#	Pa_HostApiDeviceIndexToDeviceIndex()
											#	to enumerate all devices for 
											#	this host API 
		PaDeviceIndex defaultInputDevice	# default input device for this
											#	host API.  The value will 
											#	be a device index ranging from
											#	0 to (Pa_GetDeviceCount()-1),
											#	or paNoDevice if no default
											#   input device is available
		PaDeviceIndex defaultOutputDevice	# default output device for 
											# 	this host API.  The value will 
											#	be a device index ranging from
											#	0 to (Pa_GetDeviceCount()-1),
											#	or paNoDevice if no default
											#   output device is available
		
	# Retrieve a pointer to a structure containing information about a specific
	#  host Api.
	#
	#  @param hostApi A valid host API index ranging from 0 to (Pa_GetHostApiCount()-1)
	#
	#  @return A pointer to an immutable PaHostApiInfo structure describing
	#  a specific host API. If the hostApi parameter is out of range or an error
	#  is encountered, the function returns NULL.
	#
	#  The returned structure is owned by the PortAudio implementation and must not
	#  be manipulated or freed. The pointer is only guaranteed to be valid between
	#  calls to Pa_Initialize() and Pa_Terminate().
	# 
	PaHostApiInfo* Pa_GetHostApiInfo(PaHostApiIndex hostApi)
	
	# Convert a static host API unique identifier, into a runtime host API index.
	#
	# @param type A unique host API identifier belonging to the PaHostApiTypeId
	# enumeration.
	#
	# @return A valid PaHostApiIndex ranging from 0 to (Pa_GetHostApiCount()-1) or,
	# a PaErrorCode (which are always negative) if PortAudio is not initialized
	# or an error is encountered.
	#
	# The paHostApiNotFound error code indicates that the host API specified by the
	# type parameter is not available.
	#
	# @see PaHostApiTypeId
	# 
	PaHostApiIndex Pa_HostApiTypeIdToHostApiIndex(PaHostApiTypeId type)

	# Convert a host-API-specific device index to standard PortAudio device index.
	# This function may be used in conjunction with the deviceCount field of
	# PaHostApiInfo to enumerate all devices for the specified host API.
	#
	# @param hostApi A valid host API index ranging from 0 to (Pa_GetHostApiCount()-1)
	#
	# @param hostApiDeviceIndex A valid per-host device index in the range
	# 0 to (Pa_GetHostApiInfo(hostApi)->deviceCount-1)
	#
	# @return A non-negative PaDeviceIndex ranging from 0 to (Pa_GetDeviceCount()-1)
	# or, a PaErrorCode (which are always negative) if PortAudio is not initialized
	# or an error is encountered.
	#
	# A paInvalidHostApi error code indicates that the host API index specified by
	# the hostApi parameter is out of range.
	#
	# A paInvalidDevice error code indicates that the hostApiDeviceIndex parameter
	# is out of range.
	#
	# @see PaHostApiInfo
	#
	PaDeviceIndex Pa_HostApiDeviceIndexToDeviceIndex(PaHostApiIndex hostApi, int hostApiDeviceIndex)
	
	
	# Structure used to return information about a host error condition.
	# 
	ctypedef struct PaHostErrorInfo:
		PaHostApiTypeId hostApiType		# the host API which returned the error code
		long errorCode					# the error code returned
		char *errorText					# a textual description of the error if
										# 	available, otherwise an empty string

	# Return information about the last host error encountered. The error
	# information returned by Pa_GetLastHostErrorInfo() will never be modified
	# asynchronously by errors occurring in other PortAudio owned threads
	# (such as the thread that manages the stream callback.)
	#
	# This function is provided as a last resort, primarily to enhance debugging
	# by providing clients with access to all available error information.
	#
	# @return A pointer to an immutable structure constaining information about
	# the host error. The values in this structure will only be valid if a
	# PortAudio function has previously returned the paUnanticipatedHostError
	# error code.
	# 
	PaHostErrorInfo* Pa_GetLastHostErrorInfo()

#	
# Device enumeration and capabilities
#

	# Retrieve the number of available devices. The number of available devices
	# may be zero.
	#
	# @return A non-negative value indicating the number of available devices or,
	# a PaErrorCode (which are always negative) if PortAudio is not initialized
	# or an error is encountered.
	# 
	PaDeviceIndex Pa_GetDeviceCount()
	
	# Retrieve the index of the default input device. The result can be
	# used in the inputDevice parameter to Pa_OpenStream().
	#
	# @return The default input device index for the default host API, or paNoDevice
	# if no default input device is available or an error was encountered.
	# 
	PaDeviceIndex Pa_GetDefaultInputDevice()
	
	# Retrieve the index of the default output device. The result can be
	# used in the outputDevice parameter to Pa_OpenStream().
	#
	# @return The default output device index for the defualt host API, or paNoDevice
	# if no default output device is available or an error was encountered.
	#
	# @note
	# On the PC, the user can specify a default device by
	# setting an environment variable. For example, to use device #1.
	# 
	# set PA_RECOMMENDED_OUTPUT_DEVICE=1
	# 
	# The user should first determine the available device ids by using
	# the supplied application "pa_devs".
	# 
	PaDeviceIndex Pa_GetDefaultOutputDevice()
	
	# The type used to represent monotonic time in seconds that can be used
	# for synchronisation. The type is used for the outTime argument to the
	# PaStreamCallback and as the result of Pa_GetStreamTime().
	#
	# @see PaStreamCallback, Pa_GetStreamTime
	# 
	ctypedef double PaTime
	
	# A type used to specify one or more sample formats. Each value indicates
	# a possible format for sound data passed to and from the stream callback,
	# Pa_ReadStream and Pa_WriteStream.
	#
	# The standard formats paFloat32, paInt16, paInt32, paInt24, paInt8
	# and paUInt8 are usually implemented by all implementations.
	#
	# The floating point representation (paFloat32) uses +1.0 and -1.0 as the
	# maximum and minimum respectively.
	#
	# paUInt8 is an unsigned 8 bit format where 128 is considered "ground"
	#
	# The paNonInterleaved flag indicates that a multichannel buffer is passed
	# as a set of non-interleaved pointers.
	#
	# @see Pa_OpenStream, Pa_OpenDefaultStream, PaDeviceInfo
	# @see paFloat32, paInt16, paInt32, paInt24, paInt8
	# @see paUInt8, paCustomFormat, paNonInterleaved
	# 
	ctypedef unsigned long PaSampleFormat
	
	cdef PaSampleFormat paFloat32
	cdef PaSampleFormat paInt16
	cdef PaSampleFormat paInt32
	cdef PaSampleFormat paInt24
	cdef PaSampleFormat paInt8
	cdef PaSampleFormat paUInt8
	cdef PaSampleFormat paCustomFormat

	# A structure providing information and capabilities of PortAudio devices.
	# Devices may support input, output or both input and output.
	#
	ctypedef struct PaDeviceInfo:
		int structVersion					# this is struct version 2
		char *name					
		PaHostApiIndex hostApi				# note this is a host API *index*, 
											#	not a type id
		int maxInputChannels
		int maxOutputChannels
		PaTime defaultLowInputLatency		# default latency values for 
		PaTime defaultLowOutputLatency		#	interactive performance
		PaTime defaultHighInputLatency		# default latency values for 
		PaTime defaultHighOutputLatency		# 	robust non-interactive 
											#	applications (e.g. playing)
											#	sound files)
		double defaultSampleRate

	# Retrieve a pointer to a PaDeviceInfo structure containing information
	# about the specified device.
	# 
	# @return A pointer to an immutable PaDeviceInfo structure. If the device
	# parameter is out of range the function returns NULL.
	#
	# @param device A valid device index in the range 0 to (Pa_GetDeviceCount()-1)
	#
	# @note PortAudio manages the memory referenced by the returned pointer,
	# the client must not manipulate or free the memory. The pointer is only
	# guaranteed to be valid between calls to Pa_Initialize() and Pa_Terminate().
	#
	# @see PaDeviceInfo, PaDeviceIndex
	#
	PaDeviceInfo* Pa_GetDeviceInfo(PaDeviceIndex device)

# Parameters for one direction (input or output) of a stream.
# 
	ctypedef struct PaStreamParameters:
		PaDeviceIndex device		# A valid device index in the range 0 to 
									#	(Pa_GetDeviceCount()-1) specifying 
									#	the device to be used or the special 
									#	constant paUseHostApiSpecificDeviceSpecification 
									# 	which indicates that the actual
									#	device(s) to use are specified in 
									# 	hostApiSpecificStreamInfo.
									#	This field must not be set to paNoDevice.
	
		int channelCount			# The number of channels of sound to be 
									#	delivered to the stream callback or 
									#	accessed by Pa_ReadStream() or 
									#	Pa_WriteStream().  It can range from 1
									#	to the value of maxInputChannels in the
									#	PaDeviceInfo record for the device 
									#	specified by the device parameter.

		PaSampleFormat sampleFormat	# The sample format of the buffer provided 
									#	to the stream callback, Pa_ReadStream() 
									#	or Pa_WriteStream(). It may be any of 
									#	the formats described by the 
									#	PaSampleFormat enumeration.
									
		PaTime suggestedLatency		# The desired latency in seconds. Where 
									#	practical, implementations should
									#	configure their latency based on these 
									#	parameters, otherwise they may choose 
									#	the closest viable latency instead. 
									#	Unless the suggested latency is greater 
									#	than the absolute upper limit for the 
									#	device, implementations should round the
									#	suggestedLatency up to the next 
									#	practical value - ie to provide an equal
									#	or higher latency than suggestedLatency 
									#	wherever possibe.  Actual latency values 
									#	for an open stream may be retrieved 
									#	using the inputLatency and outputLatency
									#	fields of the PaStreamInfo structure
									#	returned by Pa_GetStreamInfo().
									#	@see default*Latency in PaDeviceInfo, 
									#	*Latency in PaStreamInfo
									
		void *hostApiSpecificStreamInfo		# An optional pointer to a host API
		 									#	specific data structure 
											#	containing additional 
											# 	information for device setup 
											# 	and/or stream processing.
											#	hostApiSpecificStreamInfo is 
											#	never required for correct 
											# 	operation, if not used it should 
											#	be set to NULL

	# Determine whether it would be possible to open a stream with the specified
	# parameters.
	#
	# @param inputParameters A structure that describes the input parameters used to
	# open a stream. The suggestedLatency field is ignored. See PaStreamParameters
	# for a description of these parameters. inputParameters must be NULL for
	# output-only streams.
	#
	# @param outputParameters A structure that describes the output parameters used
	# to open a stream. The suggestedLatency field is ignored. See PaStreamParameters
	# for a description of these parameters. outputParameters must be NULL for
	# input-only streams.
	#
	# @param sampleRate The required sampleRate. For full-duplex streams it is the
	# sample rate for both input and output
	#
	# @return Returns 0 if the format is supported, and an error code indicating why
	# the format is not supported otherwise. The constant paFormatIsSupported is
	# provided to compare with the return value for success.
	#
	# @see paFormatIsSupported, PaStreamParameters
	# 
	PaError Pa_IsFormatSupported(PaStreamParameters *inputParameters, PaStreamParameters *outputParameters, double sampleRate)

#
# Streaming types and functions 
#

	#  A single PaStream can provide multiple channels of real-time
	#  streaming audio input and output to a client application. A stream
	#  provides access to audio hardware represented by one or more
	#  PaDevices. Depending on the underlying Host API, it may be possible
	#  to open multiple streams using the same device, however this behavior
	#  is implementation defined. Portable applications should assume that
	#  a PaDevice may be simultaneously used by at most one PaStream.
	#
	#  Pointers to PaStream objects are passed between PortAudio functions that
	#  operate on streams.
	#
	#  @see Pa_OpenStream, Pa_OpenDefaultStream, Pa_OpenDefaultStream, Pa_CloseStream,
	#  Pa_StartStream, Pa_StopStream, Pa_AbortStream, Pa_IsStreamActive,
	#  Pa_GetStreamTime, Pa_GetStreamCpuLoad
	#
	# typedef void PaStream;
	ctypedef void PaStream

	# Flags used to control the behavior of a stream. They are passed as
	# parameters to Pa_OpenStream or Pa_OpenDefaultStream. Multiple flags may be
	# ORed together.
	#
	# @see Pa_OpenStream, Pa_OpenDefaultStream
	# @see paNoFlag, paClipOff, paDitherOff, paNeverDropInput,
	# paPrimeOutputBuffersUsingStreamCallback, paPlatformSpecificFlags
	# 
	# typedef unsigned long PaStreamFlags;
	ctypedef unsigned long PaStreamFlags

	cdef PaStreamFlags paNoFlag
	cdef PaStreamFlags paClipOff
	cdef PaStreamFlags paDitherOff
	cdef PaStreamFlags paNeverDropInput
	cdef PaStreamFlags paPrimeOutputBuffersUsingStreamCallback
	cdef PaStreamFlags paPlatformSpecificFlags
	cdef PaStreamFlags paNonInterleaved
	
	# 
	# Timing information for the buffers passed to the stream callback.
	# 
	# typedef struct PaStreamCallbackTimeInfo{
	#	  PaTime inputBufferAdcTime;
	#	  PaTime currentTime;
	#	  PaTime outputBufferDacTime;
	# } PaStreamCallbackTimeInfo;
	ctypedef struct PaStreamCallbackTimeInfo:
		PaTime inputBufferAdcTime
		PaTime currentTime
		PaTime outputBufferDacTime

	# Flag bit constants for the statusFlags to PaStreamCallback.
	#
	# @see paInputUnderflow, paInputOverflow, paOutputUnderflow, paOutputOverflow,
	# paPrimingOutput
	# 
	# typedef unsigned long PaStreamCallbackFlags;
	ctypedef unsigned long PaStreamCallbackFlags

	cdef PaStreamCallbackFlags paInputUnderflow
	cdef PaStreamCallbackFlags paInputOverflow
	cdef PaStreamCallbackFlags paOutputUnderflow
	cdef PaStreamCallbackFlags paOutputOverflow
	cdef PaStreamCallbackFlags paPrimingOutput
	
	# Allowable return values for the PaStreamCallback.
	# @see PaStreamCallback
	# 
	# typedef enum PaStreamCallbackResult
	# {
	#	  paContinue=0,
	#	  paComplete=1,
	#	  paAbort=2
	# } PaStreamCallbackResult;
	ctypedef enum PaStreamCallbackResult:
		paContinue=0
		paComplete=1
		paAbort=2

	# Functions of type PaStreamCallback are implemented by PortAudio clients.
	# They consume, process or generate audio in response to requests from an
	# active PortAudio stream.
	#
	# @param input and @param output are arrays of interleaved samples,
	# the format, packing and number of channels used by the buffers are
	# determined by parameters to Pa_OpenStream().
	#
	# @param frameCount The number of sample frames to be processed by
	# the stream callback.
	#
	# @param timeInfo The time in seconds when the first sample of the input
	# buffer was received at the audio input, the time in seconds when the first
	# sample of the output buffer will begin being played at the audio output, 
	# and the time in seconds when the stream callback was called.
	# See also Pa_GetStreamTime()
	#
	# @param statusFlags Flags indicating whether input and/or output buffers
	# have been inserted or will be dropped to overcome underflow or overflow
	# conditions.
	#
	# @param userData The value of a user supplied pointer passed to 
	# Pa_OpenStream() intended for storing synthesis data etc.
	#
	# @return
	# The stream callback should return one of the values in the
	# PaStreamCallbackResult enumeration. To ensure that the callback continues
	# to be called, it should return paContinue (0). Either paComplete or paAbort
	# can be returned to finish stream processing, after either of these values 
	# is returned the callback will not be called again. If paAbort is returned 
	# the stream will finish as soon as possible. If paComplete is returned, the 
	# stream will continue until all buffers generated by the callback have been
	# played.  This may be useful in applications such as soundfile players where
	# a specific duration of output is required. However, it is not necessary 
	# to utilise this mechanism as Pa_StopStream(), Pa_AbortStream() or 
	# Pa_CloseStream() can also be used to stop the stream. The callback must 
	# always fill the entire output buffer irrespective of its return value.
	#
	# @see Pa_OpenStream, Pa_OpenDefaultStream
	#
	# @note With the exception of Pa_GetStreamCpuLoad() it is not permissable 
	# to call PortAudio API functions from within the stream callback.
	# 
	ctypedef int PaStreamCallback(void *input, void *output, unsigned long frameCount, PaStreamCallbackTimeInfo* timeInfo, PaStreamCallbackFlags statusFlags, void *userData)

	
	# Opens a stream for either input, output or both.
	#
	# @param stream The address of a PaStream pointer which will receive
	# a pointer to the newly opened stream.
	#
	# @param inputParameters A structure that describes the input parameters 
	# used by the opened stream. See PaStreamParameters for a description of 
	# these parameters. inputParameters must be NULL for output-only streams.
	#
	# @param outputParameters A structure that describes the output parameters 
	# used by the opened stream. See PaStreamParameters for a description of 
	# these parameters.  outputParameters must be NULL for input-only streams.
	#
	# @param sampleRate The desired sampleRate. For full-duplex streams it is 
	# the sample rate for both input and output
	#
	# @param framesPerBuffer The number of frames passed to the stream callback
	# function, or the preferred block granularity for a blocking read/write 
	# stream.  The special value paFramesPerBufferUnspecified (0) may be used 
	# to request that the stream callback will recieve an optimal (and possibly 
	# varying) number of frames based on host requirements and the requested 
	# latency settings.  Note: With some host APIs, the use of non-zero 
	# framesPerBuffer for a callback stream may introduce an additional layer 
	# of buffering which could introduce additional latency. PortAudio 
	# guarantees that the additional latency will be kept to the theoretical 
	# minimum however, it is strongly recommended that a non-zero framesPerBuffer
	# value only be used when your algorithm requires a fixed number of frames
	# per stream callback.
	#
	# @param streamFlags Flags which modify the behaviour of the streaming 
	# process.  This parameter may contain a combination of flags ORed together.
	# Some flags may only be relevant to certain buffer formats.
	#
	# @param streamCallback A pointer to a client supplied function that is 
	# responsible for processing and filling input and output buffers. If this
	# parameter is NULL the stream will be opened in 'blocking read/write' mode.
	# In blocking mode, the client can receive sample data using Pa_ReadStream 
	# and write sample data using Pa_WriteStream, the number of samples that 
	# may be read or written without blocking is returned by 
	# Pa_GetStreamReadAvailable and Pa_GetStreamWriteAvailable respectively.
	#
	# @param userData A client supplied pointer which is passed to the stream 
	# callback function. It could for example, contain a pointer to instance 
	# data necessary for processing the audio buffers. This parameter is ignored
	# if streamCallback is NULL.
	#
	# @return
	# Upon success Pa_OpenStream() returns paNoError and places a pointer to a
	# valid PaStream in the stream argument. The stream is inactive (stopped).
	# If a call to Pa_OpenStream() fails, a non-zero error code is returned (see
	# PaError for possible error codes) and the value of stream is invalid.
	#
	# @see PaStreamParameters, PaStreamCallback, Pa_ReadStream, Pa_WriteStream,
	# Pa_GetStreamReadAvailable, Pa_GetStreamWriteAvailable
	# 
	PaError Pa_OpenStream(PaStream** stream, PaStreamParameters *inputParameters, PaStreamParameters *outputParameters, double sampleRate, unsigned long framesPerBuffer, PaStreamFlags streamFlags, PaStreamCallback *streamCallback, void *userData ) nogil
	
	# A simplified version of Pa_OpenStream() that opens the default input
	# and/or output devices.
	#
	# @param stream The address of a PaStream pointer which will receive a 
	# pointer to the newly opened stream.
	#
	# @param numInputChannels	The number of channels of sound that will be 
	# supplied to the stream callback or returned by Pa_ReadStream. It can 
	# range from 1 to the value of maxInputChannels in the PaDeviceInfo record
	# for the default input device. If 0 the stream is opened as an output-only 
	# stream.
	#
	# @param numOutputChannels The number of channels of sound to be delivered 
	# to the stream callback or passed to Pa_WriteStream. It can range from 1 
	# to the value of maxOutputChannels in the PaDeviceInfo record for the 
	# default output dvice.  If 0 the stream is opened as an output-only stream.
	#
	# @param sampleFormat The sample format of both the input and output buffers
	# provided to the callback or passed to and from Pa_ReadStream and 
	# Pa_WriteStream.
	# sampleFormat may be any of the formats described by the PaSampleFormat
	# enumeration.
	#
	# @param sampleRate Same as Pa_OpenStream parameter of the same name.
	# @param framesPerBuffer Same as Pa_OpenStream parameter of the same name.
	# @param streamCallback Same as Pa_OpenStream parameter of the same name.
	# @param userData Same as Pa_OpenStream parameter of the same name.
	#
	# @return As for Pa_OpenStream
	#
	# @see Pa_OpenStream, PaStreamCallback
	# 
	PaError Pa_OpenDefaultStream(PaStream** stream, int numInputChannels, int numOutputChannels, PaSampleFormat sampleFormat, double sampleRate, unsigned long framesPerBuffer, PaStreamCallback *streamCallback, void *userData) nogil

	# Closes an audio stream. If the audio stream is active it
	# discards any pending buffers as if Pa_AbortStream() had been called.
	# 
	# PaError Pa_CloseStream( PaStream *stream );
	PaError Pa_CloseStream(PaStream *stream) nogil

	# Functions of type PaStreamFinishedCallback are implemented by PortAudio
	# clients. They can be registered with a stream using the 
	# Pa_SetStreamFinishedCallback function. Once registered they are called 
	# when the stream becomes inactive (ie once a call to Pa_StopStream() will 
	# not block).  A stream will become inactive after the stream callback 
	# returns non-zero, or when Pa_StopStream or Pa_AbortStream is called. For 
	# a stream providing audio output, if the stream callback returns paComplete, 
	# or Pa_StopStream is called, the stream finished callback will not be 
	# called until all generated sample data has been played.
	#
	# @param userData The userData parameter supplied to Pa_OpenStream()
	#
	# @see Pa_SetStreamFinishedCallback
	# 
	ctypedef void PaStreamFinishedCallback(void *userData) nogil

	# Register a stream finished callback function which will be called when the
	# stream becomes inactive. See the description of PaStreamFinishedCallback 
	# for further details about when the callback will be called.
	#
	# @param stream a pointer to a PaStream that is in the stopped state - if 
	# the stream is not stopped, the stream's finished callback will remain 
	# unchanged and an error code will be returned.
	#
	# @param streamFinishedCallback a pointer to a function with the same 
	# signature as PaStreamFinishedCallback, that will be called when the 
	# stream becomes inactive. Passing NULL for this parameter will un-register
	# a previously registered stream finished callback function.
	#
	# @return on success returns paNoError, otherwise an error code indicating the cause
	# of the error.
	#
	# @see PaStreamFinishedCallback
	# 
	PaError Pa_SetStreamFinishedCallback(PaStream* stream, PaStreamFinishedCallback* streamFinishedCallback) nogil
	
	# Commences audio processing.
	# 
	# PaError Pa_StartStream( PaStream *stream );
	PaError Pa_StartStream(PaStream *stream) nogil

	# Terminates audio processing. It waits until all pending
	# audio buffers have been played before it returns.
	# 
	# PaError Pa_StopStream( PaStream *stream );
	PaError Pa_StopStream(PaStream *stream) nogil

	# Terminates audio processing immediately without waiting for pending
	# buffers to complete.
	# 
	# PaError Pa_AbortStream( PaStream *stream );
	PaError Pa_AbortStream(PaStream *stream) nogil

	# Determine whether the stream is stopped.
	# A stream is considered to be stopped prior to a successful call to
	# Pa_StartStream and after a successful call to Pa_StopStream or 
	# Pa_AbortStream.  If a stream callback returns a value other than 
	# paContinue the stream is NOT considered to be stopped.
	#
	# @return Returns one (1) when the stream is stopped, zero (0) when
	# the stream is running or, a PaErrorCode (which are always negative) if
	# PortAudio is not initialized or an error is encountered.
	#
	# @see Pa_StopStream, Pa_AbortStream, Pa_IsStreamActive
	# 
	# PaError Pa_IsStreamStopped( PaStream *stream );
	PaError Pa_IsStreamStopped(PaStream *stream) nogil

	# Determine whether the stream is active.
	# A stream is active after a successful call to Pa_StartStream(), until it
	# becomes inactive either as a result of a call to Pa_StopStream() or
	# Pa_AbortStream(), or as a result of a return value other than paContinue 
	# from the stream callback. In the latter case, the stream is considered 
	# inactive after the last buffer has finished playing.
	#
	# @return Returns one (1) when the stream is active (ie playing or 
	# recording audio), zero (0) when not playing or, a PaErrorCode (which are 
	# always negative) if PortAudio is not initialized or an error is 
	# encountered.
	#
	# @see Pa_StopStream, Pa_AbortStream, Pa_IsStreamStopped
	# 
	# PaError Pa_IsStreamActive( PaStream *stream );
	PaError Pa_IsStreamActive(PaStream *stream) nogil
	
	# A structure containing unchanging information about an open stream.
	# @see Pa_GetStreamInfo
	# 
	ctypedef struct PaStreamInfo:
		int structVersion		# this is struct version 1
		PaTime inputLatency		# The input latency of the stream in seconds. 
								#	This value provides the most accurate 
								#	estimate of input latency available to the
								#	implementation. It may differ significantly 
								#	from the suggestedLatency value passed to 
								#	Pa_OpenStream().  The value of this field 
								#	will be zero (0.) for output-only streams.
								#	@see PaTime
		PaTime outputLatency	# The output latency of the stream in seconds. 
								#	This value provides the most accurate 
								#	estimate of output latency available to the
								#	implementation. It may differ significantly 
								#	from the suggestedLatency value passed to 
								#	Pa_OpenStream().  The value of this field 
								#	will be zero (0.) for input-only streams.
								#	@see PaTime
		double sampleRate		# The sample rate of the stream in Hertz 
								#	(samples per second). In cases where the 
								#	hardware sample rate is inaccurate and 
								#	PortAudio is aware of it, the value of this
								#	field may be different from the sampleRate 
								#	parameter passed to Pa_OpenStream(). If 
								#	information about the actual hardware sample
								#	rate is not available, this field will have 
								#	the same value as the sampleRate parameter 
								#	passed to Pa_OpenStream().
	
	# Retrieve a pointer to a PaStreamInfo structure containing information
	# about the specified stream.
	# @return A pointer to an immutable PaStreamInfo structure. If the stream
	# parameter invalid, or an error is encountered, the function returns NULL.
	#
	# @param stream A pointer to an open stream previously created with Pa_OpenStream.
	#
	# @note PortAudio manages the memory referenced by the returned pointer,
	# the client must not manipulate or free the memory. The pointer is only
	# guaranteed to be valid until the specified stream is closed.
	#
	# @see PaStreamInfo
	# 
	# const PaStreamInfo* Pa_GetStreamInfo( PaStream *stream );
	PaStreamInfo* Pa_GetStreamInfo(PaStream *stream) nogil

	# Determine the current time for the stream according to the same clock used
	# to generate buffer timestamps. This time may be used for syncronising other
	# events to the audio stream, for example synchronizing audio to MIDI.
	#
	# @return The stream's current time in seconds, or 0 if an error occurred.
	#
	# @see PaTime, PaStreamCallback
	# 
	# PaTime Pa_GetStreamTime( PaStream *stream );
	PaTime Pa_GetStreamTime(PaStream* stream) nogil

	# Retrieve CPU usage information for the specified stream.
	# The "CPU Load" is a fraction of total CPU time consumed by a callback stream's
	# audio processing routines including, but not limited to the client supplied
	# stream callback. This function does not work with blocking read/write streams.
	#
	# This function may be called from the stream callback function or the
	# application.
	#
	# @return
	# A floating point value, typically between 0.0 and 1.0, where 1.0 indicates
	# that the stream callback is consuming the maximum number of CPU cycles possible
	# to maintain real-time operation. A value of 0.5 would imply that PortAudio and
	# the stream callback was consuming roughly 50% of the available CPU time. The
	# return value may exceed 1.0. A value of 0.0 will always be returned for a
	# blocking read/write stream, or if an error occurrs.
	# 
	# double Pa_GetStreamCpuLoad( PaStream* stream );
	double Pa_GetStreamCpuLoad(PaStream* stream) nogil

	# Read samples from an input stream. The function doesn't return until
	# the entire buffer has been filled - this may involve waiting for the operating
	# system to supply the data.
	#
	# @param stream A pointer to an open stream previously created with Pa_OpenStream.
	#
	# @param buffer A pointer to a buffer of sample frames. The buffer contains
	# samples in the format specified by the inputParameters->sampleFormat field
	# used to open the stream, and the number of channels specified by
	# inputParameters->numChannels. If non-interleaved samples were requested,
	# buffer is a pointer to the first element of an array of non-interleaved
	# buffer pointers, one for each channel.
	#
	# @param frames The number of frames to be read into buffer. This parameter
	# is not constrained to a specific range, however high performance applications
	# will want to match this parameter to the framesPerBuffer parameter used
	# when opening the stream.
	#
	# @return On success PaNoError will be returned, or PaInputOverflowed if input
	# data was discarded by PortAudio after the previous call and before this call.
	# 
	# PaError Pa_ReadStream( PaStream* stream,
	#						 void *buffer,
	#						 unsigned long frames );
	PaError Pa_ReadStream(PaStream* stream, void *buffer, unsigned long frames) nogil

	# Write samples to an output stream. This function doesn't return until the
	# entire buffer has been consumed - this may involve waiting for the operating
	# system to consume the data.
	#
	# @param stream A pointer to an open stream previously created with Pa_OpenStream.
	#
	# @param buffer A pointer to a buffer of sample frames. The buffer contains
	# samples in the format specified by the outputParameters->sampleFormat field
	# used to open the stream, and the number of channels specified by
	# outputParameters->numChannels. If non-interleaved samples were requested,
	# buffer is a pointer to the first element of an array of non-interleaved
	# buffer pointers, one for each channel.
	#
	# @param frames The number of frames to be written from buffer. This parameter
	# is not constrained to a specific range, however high performance applications
	# will want to match this parameter to the framesPerBuffer parameter used
	# when opening the stream.
	#
	# @return On success PaNoError will be returned, or paOutputUnderflowed if
	# additional output data was inserted after the previous call and before this
	# call.
	# 
	# PaError Pa_WriteStream( PaStream* stream,
	#						  const void *buffer,
	#						  unsigned long frames );
	PaError Pa_WriteStream(PaStream* stream, void *buffer, unsigned long frames) nogil


	# Retrieve the number of frames that can be read from the stream without
	# waiting.
	#
	# @return Returns a non-negative value representing the maximum number of frames
	# that can be read from the stream without blocking or busy waiting or, a
	# PaErrorCode (which are always negative) if PortAudio is not initialized or an
	# error is encountered.
	# 
	# signed long Pa_GetStreamReadAvailable( PaStream* stream );
	signed long Pa_GetStreamReadAvailable(PaStream* stream) nogil

	# Retrieve the number of frames that can be written to the stream without
	# waiting.
	#
	# @return Returns a non-negative value representing the maximum number of frames
	# that can be written to the stream without blocking or busy waiting or, a
	# PaErrorCode (which are always negative) if PortAudio is not initialized or an
	# error is encountered.
	# 
	# signed long Pa_GetStreamWriteAvailable( PaStream* stream );
	signed long Pa_GetStreamWriteAvailable(PaStream* stream) nogil

#
# Miscellaneous utilities
#

	# Retrieve the size of a given sample format in bytes.
	#
	# @return The size in bytes of a single sample in the specified format,
	# or paSampleFormatNotSupported if the format is not supported.
	# 
	# PaError Pa_GetSampleSize( PaSampleFormat format );
	PaError Pa_GetSampleSize(PaSampleFormat format) nogil

	# Put the caller to sleep for at least 'msec' milliseconds. This function 
	# is provided only as a convenience for authors of portable code (such as 
	# the tests and examples in the PortAudio distribution.)
	#
	# The function may sleep longer than requested so don't rely on this for 
	# accurate musical timing.
	# 
	# void Pa_Sleep( long msec );
	void Pa_Sleep(long msec) 
	
#
# Callback stuff
#	
cdef int Pa_StreamCallbackWrapper(void *inputBuffer, void *outputBuffer, unsigned long framesPerBuffer, PaStreamCallbackTimeInfo* timeInfo, PaStreamCallbackFlags statusFlags, void *userData ) with gil:
	#cdef float **tmpPtr
	cdef PyGILState_STATE st
	cdef float *tmpPtr
	cdef float *headPtr
	cdef float foo
	
	pyOut = None
	pyErr = None
	
	pyInputBuffer = PyCObject_FromVoidPtr(inputBuffer, NULL)
	cbs = <object>(userData)
	
	(pyErr, pyOut) = (cbs['streamcallback'])(pyInputBuffer, framesPerBuffer, None, statusFlags) 
	tmpPtr = <float *>outputBuffer
	headPtr = tmpPtr
	for i in range(0, len(pyOut)):
		tmpPtr[0] = pyOut[i] #<float>(pyOut[i])
		tmpPtr = tmpPtr+1
	tmpPtr = headPtr	
	outputBuffer = <void *>tmpPtr
	
	return pyErr

	
cdef void Pa_StreamFinishedCallbackWrapper(void *userData) with gil:
	cbs = <object>(userData) #PyCObject_FromVoidPtr(userData, NULL)
	if (cbs['finishedcallback']):
		cbs['finishedcallback']()
	
#
#
# -------------- Python Interface -----------
#
#

# @see PaErrorCode	
pyPaNoError = paNoError
pyPaNotInitialized = paNotInitialized
pyPaUnanticipatedHostError = paUnanticipatedHostError
pyPaInvalidChannelCount = paInvalidChannelCount
pyPaInvalidSampleRate = paInvalidSampleRate
pyPaInvalidDevice = paInvalidDevice
pyPaInvalidFlag = paInvalidFlag
pyPaSampleFormatNotSupported = paSampleFormatNotSupported
pyPaBadIODeviceCombination = paBadIODeviceCombination
pyPaInsufficientMemory = paInsufficientMemory
pyPaBufferTooBig = paBufferTooBig
pyPaBufferTooSmall = paBufferTooSmall
pyPaNullCallback = paNullCallback
pyPaBadStreamPtr = paBadStreamPtr
pyPaTimedOut = paTimedOut
pyPaInternalError = paInternalError
pyPaDeviceUnavailable = paDeviceUnavailable
pyPaIncompatibleHostApiSpecificStreamInfo = paIncompatibleHostApiSpecificStreamInfo
pyPaStreamIsStopped = paStreamIsStopped
pyPaStreamIsNotStopped = paStreamIsNotStopped
pyPaInputOverflowed = paInputOverflowed
pyPaOutputUnderflowed = paOutputUnderflowed
pyPaHostApiNotFound = paHostApiNotFound
pyPaInvalidHostApi = paInvalidHostApi
pyPaCanNotReadFromACallbackStream = paCanNotReadFromACallbackStream
pyPaCanNotWriteToACallbackStream = paCanNotWriteToACallbackStream
pyPaCanNotReadFromAnOutputOnlyStream = paCanNotReadFromAnOutputOnlyStream
pyPaCanNotWriteToAnInputOnlyStream = paCanNotWriteToAnInputOnlyStream
pyPaIncompatibleStreamHostApi = paIncompatibleStreamHostApi
pyPaBadBufferPtr = paBadBufferPtr

# A special PaDeviceIndex value indicating that no device is available,
# or should be used.
#
# @see PaDeviceIndex
# 
# #define paNoDevice ((PaDeviceIndex)-1)
pyPaNoDevice = paNoDevice
	

# A special PaDeviceIndex value indicating that the device(s) to be used
# are specified in the host api specific stream info structure.
#
# @see PaDeviceIndex
# 
# #define paUseHostApiSpecificDeviceSpecification ((PaDeviceIndex)-2)
pyPaUseHostApiSpecificDeviceSpecification = paUseHostApiSpecificDeviceSpecification

#
# @see PaHostApiTypeId
pyPaInDevelopment = paInDevelopment
pyPaDirectSound = paDirectSound
pyPaMME = paMME
pyPaASIO = paASIO
pyPaSoundManager = paSoundManager
pyPaCoreAudio = paCoreAudio
pyPaOSS = paOSS
pyPaALSA = paALSA
pyPaAL = paAL
pyPaBeOS = paBeOS
pyPaWDMKS = paWDMKS
pyPaJACK = paJACK
pyPaWASAPI = paWASAPI
pyPaAudioScienceHPI = paAudioScienceHPI

#
# @see PaSampleFormat
pyPaFloat32 		= paFloat32
pyPaInt32 			= paInt32
pyPaInt24			= paInt24
pyPaInt16			= paInt16
pyPaInt8			= paInt8
pyPaUInt8			= paUInt8
pyPaCustomFormat	= paCustomFormat

# @see PaStreamFlags
pyPaNoFlag		= paNoFlag

# Disable default clipping of out of range samples.
# @see PaStreamFlags
pyPaClipOff		= paClipOff

# Disable default dithering.
# @see PaStreamFlags
pyPaDitherOff		= paDitherOff

# Flag requests that where possible a full duplex stream will not discard
# overflowed input samples without calling the stream callback. This flag is
# only valid for full duplex callback streams and only when used in combination
# with the paFramesPerBufferUnspecified (0) framesPerBuffer parameter. Using
# this flag incorrectly results in a paInvalidFlag error being returned from
# Pa_OpenStream and Pa_OpenDefaultStream.
#
# @see PaStreamFlags, paFramesPerBufferUnspecified
pyPaNeverDropInput = paNeverDropInput

# Call the stream callback to fill initial output buffers, rather than the
# default behavior of priming the buffers with zeros (silence). This flag has
# no effect for input-only and blocking read/write streams.
#
# @see PaStreamFlags
pyPaPrimeOutputBuffersUsingStreamCallback = paPrimeOutputBuffersUsingStreamCallback


# A mask specifying the platform specific bits.
# @see PaStreamFlags
pyPaPlatformSpecificFlags = paPlatformSpecificFlags
pyPaNonInterleaved = paNonInterleaved

# In a stream opened with paFramesPerBufferUnspecified, indicates that
# input data is all silence (zeros) because no real data is available. In a
# stream opened without paFramesPerBufferUnspecified, it indicates that one or
# more zero samples have been inserted into the input buffer to compensate
# for an input underflow.
# @see PaStreamCallbackFlags
pyPaInputUnderflow	= paInputUnderflow

# In a stream opened with paFramesPerBufferUnspecified, indicates that data
# prior to the first sample of the input buffer was discarded due to an
# overflow, possibly because the stream callback is using too much CPU time.
# Otherwise indicates that data prior to one or more samples in the
# input buffer was discarded.
# @see PaStreamCallbackFlags
pyPaInputOverflow	= paInputOverflow

# Indicates that output data (or a gap) was inserted, possibly because the
# stream callback is using too much CPU time.
# @see PaStreamCallbackFlags
pyPaOutputUnderflow	= paOutputUnderflow

# Indicates that output data will be discarded because no room is available.
# @see PaStreamCallbackFlags
pyPaOutputOverflow	= paOutputOverflow

# Some of all of the output data will be used to prime the stream, input
# data may be zero.
# @see PaStreamCallbackFlags
pyPaPrimingOutput		= paPrimingOutput

# Return code for Pa_IsFormatSupported indicating success. 
pyPaFormatIsSupported = 0

# Can be passed as the framesPerBuffer parameter to Pa_OpenStream()
# or Pa_OpenDefaultStream() to indicate that the stream callback will
# accept buffers of any size.
# 
pyPaFramesPerBufferUnspecified = 0

# Allowable return values for the PaStreamCallback.
# @see PaStreamCallback
pyPaContinue = paContinue
pyPaComplete = paComplete
pyPaAbort = paAbort
	
#
def paGetVersion():
	versionNum = Pa_GetVersion()
	return versionNum

#	
def paGetVersionText():
	versionString = Pa_GetVersionText()
	return versionString

#	
def paGetErrorText(errCode):
	errorString = Pa_GetErrorText(errCode)
	return errorString

#	
def paInitialize():
	PyEval_InitThreads()
	errCode = Pa_Initialize()
	
	return errCode

#	
def paTerminate():
	errCode = Pa_Terminate()
	
	return errCode

#	
def paGetHostApiCount():
	apiCount = Pa_GetHostApiCount()
	return apiCount

#	
def paGetDefaultHostApi():
	defaultHostApi = Pa_GetDefaultHostApi()
	return defaultHostApi

#
def paGetHostApiInfo(hostApiIndex):
	cdef PaHostApiInfo *hostApiInfo 
	pyHostApiInfoDict = {}
	
	# WARN: 'const' casted away to avoid compiler warnings.  Do NOT change value
	hostApiInfo = <PaHostApiInfo *>Pa_GetHostApiInfo(hostApiIndex)
	pyHostApiInfoDict['structVersion'] = hostApiInfo.structVersion
	pyHostApiInfoDict['type'] = hostApiInfo.type
	pyHostApiInfoDict['name'] = hostApiInfo.name
	pyHostApiInfoDict['deviceCount'] = hostApiInfo.deviceCount
	pyHostApiInfoDict['defaultInputDevice'] = hostApiInfo.defaultInputDevice
	pyHostApiInfoDict['defaultOutputDevice'] = hostApiInfo.defaultOutputDevice
	
	return pyHostApiInfoDict

#
def paHostApiTypeIdToHostApiIndex(typeId):
	hostIndex = Pa_HostApiTypeIdToHostApiIndex(typeId)
	return hostIndex

#
def paHostApiDeviceIndexToDeviceIndex(hostApi, hostApiDeviceIndex):
	devIndex = Pa_HostApiDeviceIndexToDeviceIndex(hostApi, hostApiDeviceIndex)
	return devIndex

#
def	paGetLastHostErrorInfo():
	cdef PaHostErrorInfo *hostErrorInfo
	pyHostErrorInfoDict = {}
	
	# WARN: 'const' casted away to avoid compiler warnings.  Do NOT change value
	hostErrorInfo = <PaHostErrorInfo *>Pa_GetLastHostErrorInfo()
	pyHostErrorInfoDict['hostApiType'] = hostErrorInfo.hostApiType
	pyHostErrorInfoDict['errorCode'] = hostErrorInfo.errorCode
	pyHostErrorInfoDict['errorText'] = hostErrorInfo.errorText
	
	return pyHostErrorInfoDict

#	
def paGetDeviceCount():
	devCount = Pa_GetDeviceCount()
	return devCount

#
def	paGetDeviceInfo(deviceIdx):
	cdef PaDeviceInfo *devInfo
	pyDevInfoDict = {}
	
	# WARN: 'const' casted away to avoid compiler warnings.  Do NOT change value
	devInfo = <PaDeviceInfo *>Pa_GetDeviceInfo(deviceIdx)
	pyDevInfoDict['structVersion'] = devInfo.structVersion
	pyDevInfoDict['name'] = devInfo.name
	pyDevInfoDict['hostApi'] = devInfo.hostApi
	pyDevInfoDict['maxInputChannels'] = devInfo.maxInputChannels
	pyDevInfoDict['maxOutputChannels'] = devInfo.maxOutputChannels
	pyDevInfoDict['defaultLowInputLatency'] = devInfo.defaultLowInputLatency
	pyDevInfoDict['defaultLowOutputLatency'] = devInfo.defaultLowOutputLatency
	pyDevInfoDict['defaultHighInputLatency'] = devInfo.defaultHighInputLatency
	pyDevInfoDict['defaultHighOutputLatency'] = devInfo.defaultHighOutputLatency
	pyDevInfoDict['defaultSampleRate'] = devInfo.defaultSampleRate
	
	return pyDevInfoDict

#	
def paGetDefaultInputDevice():
	inputDev = Pa_GetDefaultInputDevice()
	return inputDev

#	
def paGetDefaultOutputDevice():
	outputDev = Pa_GetDefaultOutputDevice()
	return outputDev

#
def paIsFormatSupported(pyInputParamDict, pyOutputParamDict, sampleRate):
	cdef PaStreamParameters inputParameters
	cdef PaStreamParameters outputParameters
	cdef PaStreamParameters *inputParamPtr
	cdef PaStreamParameters *outputParamPtr
	cdef void *inputHostApiSpecificStreamInfoPtr 
	cdef void *outputHostApiSpecificStreamInfoPtr 
	
	if (pyInputParamDict):
		inputParameters.device = pyInputParamDict['device']
		inputParameters.channelCount = pyInputParamDict['channelCount']
		inputParameters.sampleFormat = pyInputParamDict['sampleFormat']
		inputParameters.suggestedLatency = pyInputParamDict['suggestedLatency']
	
		if (pyInputParamDict['hostApiSpecificStreamInfo']):
			inputHostApiSpecificStreamInfoPtr = <void *>pyInputParamDict['hostApiSpecificStreamInfo']
		else:
			inputHostApiSpecificStreamInfoPtr = NULL
			
		inputParameters.hostApiSpecificStreamInfo = inputHostApiSpecificStreamInfoPtr
		inputParamPtr = &inputParameters
	else:
		inputParamPtr = NULL
		
	if (pyOutputParamDict):	
		outputParameters.device = pyOutputParamDict['device']
		outputParameters.channelCount = pyOutputParamDict['channelCount']
		outputParameters.sampleFormat = pyOutputParamDict['sampleFormat']
		outputParameters.suggestedLatency = pyOutputParamDict['suggestedLatency']
		if (pyOutputParamDict['hostApiSpecificStreamInfo']):
			outputHostApiSpecificStreamInfoPtr = <void *>pyOutputParamDict['hostApiSpecificStreamInfo']
		else:
			outputHostApiSpecificStreamInfoPtr = NULL
			
		outputParameters.hostApiSpecificStreamInfo = outputHostApiSpecificStreamInfoPtr
		outputParamPtr = &outputParameters
	else:
		outputParamPtr = NULL
		
	error = Pa_IsFormatSupported(inputParamPtr, outputParamPtr, sampleRate)

	return error

#	
def paOpenStream(pyInputParamDict, pyOutputParamDict, sampleRate, framesPerBuffer, streamFlags, pyUserData):
	cdef PaStreamParameters inputParameters
	cdef PaStreamParameters *inputParamPtr
	cdef PaStreamParameters outputParameters
	cdef PaStreamParameters *outputParamPtr
	
	cdef void *inputHostApiSpecificStreamInfoPtr 
	cdef void *outputHostApiSpecificStreamInfoPtr 
	cdef PaStream *streamPtr
	cdef PaStreamCallback *streamCallbackPtr
	cdef void *userDataPtr
	cdef void *returnStream
	
	pyUserDataDict = {}
	
	pyStream = None
	
	if (pyInputParamDict):
		inputParameters.device = pyInputParamDict['device']
		inputParameters.channelCount = pyInputParamDict['channelCount']
		inputParameters.sampleFormat = pyInputParamDict['sampleFormat']
		inputParameters.suggestedLatency = pyInputParamDict['suggestedLatency']
	
		if (pyInputParamDict['hostApiSpecificStreamInfo']):
			inputHostApiSpecificStreamInfoPtr = <void *>pyInputParamDict['hostApiSpecificStreamInfo']
		else:
			inputHostApiSpecificStreamInfoPtr = NULL
			
		inputParameters.hostApiSpecificStreamInfo = inputHostApiSpecificStreamInfoPtr
		inputParamPtr = &inputParameters
	else:
		inputParamPtr = NULL
	
	if (pyOutputParamDict):
		outputParameters.device = pyOutputParamDict['device']
		outputParameters.channelCount = pyOutputParamDict['channelCount']
		outputParameters.sampleFormat = pyOutputParamDict['sampleFormat']
		outputParameters.suggestedLatency = pyOutputParamDict['suggestedLatency']
	
		if (pyOutputParamDict['hostApiSpecificStreamInfo']):
			outputHostApiSpecificStreamInfoPtr = <void *>pyOutputParamDict['hostApiSpecificStreamInfo']
		else:
			outputHostApiSpecificStreamInfoPtr = NULL
			
		outputParameters.hostApiSpecificStreamInfo = outputHostApiSpecificStreamInfoPtr
		outputParamPtr = &outputParameters
	else:
		outputParamPtr = NULL

	streamPtr = <PaStream *>pyStream

	if (pyUserData):
		userDataPtr = <void *>pyUserData
	else:
		userDataPtr = NULL
			
	streamCallbackPtr = <PaStreamCallback *>Pa_StreamCallbackWrapper
	error = Pa_OpenStream(&streamPtr, inputParamPtr, outputParamPtr, sampleRate, framesPerBuffer, streamFlags, streamCallbackPtr, userDataPtr) #NULL, NULL) #streamCallbackPtr, NULL) #userDataPtr)
	returnStream = <void *>streamPtr
	pyStream = PyCObject_FromVoidPtr(returnStream, NULL)
	return error, pyStream 
	
#
def paOpenDefaultStream(numInputChannels, numOutputChannels, sampleFormat, sampleRate, framesPerBuffer, pyUserData):
	cdef PaStream *streamPtr
	cdef PaStreamCallback *streamCallbackPtr
	cdef void *userDataPtr
	cdef void *returnStream
	
	pyStream = None
	
	streamPtr = <PaStream *>pyStream
	
	if (pyUserData):
		userDataPtr = <void *>pyUserData[0]
	else:
		userDataPtr = NULL
	
	streamCallbackPtr = <PaStreamCallback *>Pa_StreamCallbackWrapper
	error = Pa_OpenDefaultStream(&streamPtr, numInputChannels, numOutputChannels, sampleFormat, sampleRate, framesPerBuffer, streamCallbackPtr, userDataPtr)
	
	returnStream = <void *>streamPtr
	pyStream = PyCObject_FromVoidPtr(returnStream, NULL)
	
	return error, pyStream

#	
def paCloseStream(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	
	error = Pa_CloseStream(streamPtr)
	return error

#
def paSetStreamFinishedCallback(pyStream, activate):
	cdef PaStream *streamPtr
	cdef PaStreamFinishedCallback *streamFinishedCallbackPtr
	
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	
	if (activate):	
		streamFinishedCallbackPtr = <PaStreamFinishedCallback *>Pa_StreamFinishedCallbackWrapper
	else:
		streamFinishedCallbackPtr = NULL
		
	error = Pa_SetStreamFinishedCallback(streamPtr, streamFinishedCallbackPtr)
	return error
	
#	
def paStartStream(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	error = Pa_StartStream(streamPtr)
	return error

#	
def paStopStream(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	error = Pa_StopStream(streamPtr)
	return error

#	
def paAbortStream(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	
	error = Pa_AbortStream(streamPtr)
	return error

#
def paIsStreamStopped(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	
	error = Pa_IsStreamStopped(streamPtr)
	return error

#
def paIsStreamActive(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)

	error = Pa_IsStreamActive(streamPtr)
	return error
	
#
def paGetStreamInfo(pyStream):
	cdef PaStream *streamPtr
	cdef PaStreamInfo *streamInfo
	
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	
	# WARN: 'const' casted away to avoid compiler warnings.  Do NOT change value
	streamInfo = <PaStreamInfo *>Pa_GetStreamInfo(streamPtr)
	
	pyStreamInfo = {}
	pyStreamInfo['structVersion'] = streamInfo.structVersion
	pyStreamInfo['inputLatency'] = streamInfo.inputLatency
	pyStreamInfo['outputLatency'] = streamInfo.outputLatency
	pyStreamInfo['sampleRate'] = streamInfo.sampleRate
	
	return pyStreamInfo

#
def paGetStreamTime(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	
	time = Pa_GetStreamTime(streamPtr)
	
	return time

#
def paGetStreamCpuLoad(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)

	cpuLoad = Pa_GetStreamCpuLoad(streamPtr)
	
	return cpuLoad
	
#
def paReadStream(pyStream, frames):
	cdef PaStream *streamPtr
	cdef void *buffer

	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)

	error = Pa_ReadStream(streamPtr, buffer, frames)

	pyBuffer = PyCObject_FromVoidPtr(buffer, NULL)

	return error, pyBuffer

#
def paWriteStream(pyStream, pyBuffer, frames):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	
	error = Pa_WriteStream(streamPtr, <void *>pyBuffer, frames)
	
	return error

#
def paGetStreamReadAvailable(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	
	maxFrames = Pa_GetStreamReadAvailable(streamPtr)
	
	return maxFrames

#
def paGetStreamWriteAvailable(pyStream):
	cdef PaStream *streamPtr
	streamPtr = <PaStream *>PyCObject_AsVoidPtr(pyStream)
	
	maxFrames = Pa_GetStreamWriteAvailable(streamPtr)
	
	return maxFrames
	
#
def paGetSampleSize(format):
	size = Pa_GetSampleSize(format)
	
	return size
	
#	
def paSleep(msec):
	sleep(msec/1000.)
	