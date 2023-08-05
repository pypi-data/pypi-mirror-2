Type TSY85Header
    'File Ident
    FileIdent As String * 10    '00: Always "SY80 WAVE1"
    Unknown1 As String * 6      '10: Guess: 00 00 00 00 00 20
    HighKeyHigh As String * 1   '16: High Key of mapped sample
    HighKeyLow As String * 1    '17: "
    OrgKey As String * 1        '18: Original Key of sample
    Unknown2 As String * 1      '19: Guess: 00
    PitchHigh As String * 1     '20: Re-tuned pitch of sample
    PitchLow As String * 1      '21: "
    Unknown3 As String * 2      '22: Guess: 00 00
    Loop As String * 1          '24: Bitwise loop info.
    SYLoopStartA As String * 1  '25: This is in ABC sequence
    SYLoopStartB As String * 1  '26:
    SYLoopStartC As String * 1  '27:

    SYLoopEndA As String * 1    '28: this is in BCA sequence
    SYLoopEndB As String * 1    '29: this is in BCA sequence
    SYLoopEndC As String * 1    '30: this is in BCA sequence

    SYSamplesA As String * 1    '31: No Of Samples - 1 in ABC sequence
    SYSamplesB As String * 1    '32: No Of Samples - 1 in ABC sequence
    SYSamplesC As String * 1    '33: o Of Samples - 1 in ABC sequence

    Volume As String * 1        '34: Attenuation of sample (127 - Volume)
    Unknown8 As String * 9      '35: Guess: 01 3F 00 00 00 28 3F 3F FF
    SampleFormat As String * 1  '44: 8 or 16 Bits
    'Period
    PeriodLow As String * 1     '45: This is reciprocal of sample
    PeriodMid As String * 1     '46: frequency stored as 7-Bit data,
    PeriodHigh As String * 1    '47: same as MIDI Sample Dump
    'Sample Length
    LengthLow As String * 1     '48: Stored as 7-Bit data
    LengthMid As String * 1     '49: same as Sample Dump
    LengthHigh As String * 1    '50:
    'Loop Start
    LoopStartLow As String * 1  '51: Stored as 7-Bit data, same
    LoopStartMid As String * 1  '52: as Sample Dump
    LoopStartHigh As String * 1 '53:
    'Loop End
    LoopEndlow As String * 1    '54: Stored as 7-Bit data, same
    LoopEndMid As String * 1    '55: As Sample Dump Protocol
    LoopEndHigh As String * 1   '56:
    Unknown9 As String * 1      '57: Always 7F
    Blocks40A As String * 1     '58: No Of 40 sample blocks
    Blocks40B As String * 1     '59: No Of 40 sample blocks
    Blocks512A As String * 1    '60: No Of 512 sample blocks
    Blocks512B As String * 1    '61: No Of 512 sample blocks
    Unknown10 As String * 2     '62: Always 00 7D
    LowKeyHigh As String * 1    '64: Low key of mapped sample
    LowKeyLow As String * 1     '65:
    'Padding
    Padding As String * 958     '66: Filled with Nulls
End Type

'Used for Input
Type TSY85Packet
    Packetdata As String * 1024
End Type


Function GetSY85() As Integer
    'Function reads an SY85 file from disk, converting to .WAV
    Dim SY85Handle As Integer
    Dim SY85Header As TSY85Header
    Dim SY85Packet As TSY85Packet
    Dim SY85Packets As Long
    Dim SamplePeriod As Long
    Dim TrailingBytes As Integer
    Dim I As Long
    Dim Offset As Long
    Dim RawDataLength As Long

    'Get the next free file number and open the file
    SY85Handle = FreeFile
    RetVal = ClearDetails()
    Open GetSave.FileName.Text For Binary As SY85Handle
    'Read the SDS header record
    Get SY85Handle, , SY85Header
    'Check static Data
    If SY85Header.FileIdent <> "SY80 WAVE1" Then
        'Couldn't locate the File ident string in header record
        MsgBox "Error: Not Recognisable as an SY85 Wave File", 64
        Close SY85Handle
        GetSY85 = False
    Else
        'Found File Ident OK. - Read the rest of the data
        'Save this directory path for next time
        ConfigPut "Paths", "SY85SourceDir", CStr(GetSave.Dir1.Path)
        WavDown.Caption = GetSave.FileName.Text
        'Sample Frequency (Inverse of Sample Period)
        SamplePeriod = Asc(SY85Header.PeriodLow) + (Asc(SY85Header.PeriodMid) * CLng(128)) + (Asc(SY85Header.PeriodHigh) * CLng(16384))
        WavDown.SampleFreq.Text = 1000000000 / SamplePeriod
        WavDown.SampleRate.Text = Format$(1000000000 / SamplePeriod, "#,###,###") & "Hz"
        'Sample Length (number of samples)
        WavDown.Samples.Text = Format$(Asc(SY85Header.LengthLow) + (Asc(SY85Header.LengthMid) * CLng(128)) + (Asc(SY85Header.LengthHigh) * CLng(16384)), "#,###,###,###")
        WavDown.NoOfSamples.Text = Asc(SY85Header.LengthLow) + (Asc(SY85Header.LengthMid) * CLng(128)) + (Asc(SY85Header.LengthHigh) * CLng(16384))
        'Sample Format
        WavDown.BitsPerSample.Text = Asc(SY85Header.SampleFormat)
        WavDown.WAVEFORMAT.Text = Asc(SY85Header.SampleFormat) & " Bit Mono" 'SY85 can't do Stereo (can it?????)
        'Loop Start
        WavDown.LoopStart.Text = Asc(SY85Header.LoopStartLow) + (Asc(SY85Header.LoopStartMid) * CLng(128)) + (Asc(SY85Header.LoopStartHigh) * CLng(16384))
        'Disable the loop start box - you can't change it anyway !!
        WavDown.LoopStart.Enabled = True
        'Loop End point
        WavDown.LoopEnd.Text = Asc(SY85Header.LoopEndlow) + (Asc(SY85Header.LoopEndMid) * CLng(128)) + (Asc(SY85Header.loopEndHigh) * CLng(16384))
        WavDown.LoopEnd.Enabled = True
        'Loop Type info
        Select Case Asc(SY85Header.Loop)
            Case &H0
            Case &H1
                WavDown.LoopType.Text = "Fwd 1-Shot"
            Case &H2
                WavDown.LoopType.Text = "Fwd Nrm Lp."
            Case &H3
                WavDown.LoopType.Text = "Fwd Alt Lp."
            Case &H4
            Case &H5
                WavDown.LoopType.Text = "Bwd 1-Shot"
            Case &H6
                WavDown.LoopType.Text = "Bwd Nrm Lp."
            Case &H7
                WavDown.LoopType.Text = "Bwd Alt Lp."
        End Select
        WavDown.SampleNumber.Text = 0
        'Mono / Stereo
        WavDown.Channels.Text = 1
        'Calculate size of resulting Raw data buffer..
        'NOTE it can only be MONO
        RawDataLength = WavDown.NoOfSamples.Text * 4
        'Allocate and lock a data buffer for this data.
        RetVal = GlobalUnlock(hglbRawData)
        hglbRawData = GlobalReAlloc(hglbRawData, RawDataLength + 4, GMEM_MOVEABLE Or GMEM_ZEROINIT)
        If hglbRawData = &H0 Then
            MsgBox "Error: Unable to allocate buffer of " & Format$(RawDataLength + 4, "#,###,###,###") & " Bytes", 48
            GetSY85 = False
        Else
            lpRawData = GlobalLock(hglbRawData)
            If lpRawData = &H0 Then
                MsgBox "Error: Unable to lock Memory buffer for Raw Data", 48
                GetSY85 = False
            Else
                RawBufferAllocated = True
                'Calculate the number of SY85 1k packets
                SY85Packets = Int(WavDown.NoOfSamples.Text / 512)   'You can get 512 SY85 samples in each 1k packet
                TrailingBytes = (WavDown.NoOfSamples.Text - (SY85Packets * 512)) * 2 '2-Bytes per sample!!
                'Read all data and convert to Raw format
                Offset = 0
                Counter.Caption = "SY85 Load"
                Counter.Frame3D1.Caption = "Converting SY85 packets, please wait"
                Counter.Show
                Counter.ConvertStatus.FloodPercent = 0
                For I = 1 To SY85Packets
                    Counter.ConvertStatus.FloodPercent = (CSng(I) / CSng(SY85Packets)) * 100

                    Get SY85Handle, , SY85Packet
                    RetVal = SY852Raw(lpRawData, Offset, SY85Packet.Packetdata, WavDown.BitsPerSample.Text, 1024)
                    Offset = Offset + (512 * 4)
                    DoEvents
                    If WavDown.DownloadFlag.Text = "Cancel" Then
                        I = SY85Packets
                        'Clear the flag immediately
                        WavDown.DownloadFlag.Text = ""
                    End If
                Next I
                'Convert the Trailing Bytes
                If TrailingBytes <> 0 Then
                    Get SY85Handle, , SY85Packet
                    RetVal = SY852Raw(lpRawData, Offset, SY85Packet.Packetdata, WavDown.BitsPerSample.Text, TrailingBytes)
                End If
                Counter.Hide
                GetSY85 = True
            End If  'Global Lock error
        End If  'Global Alloc error
    End If  'Header not recognisable
    Close SY85Handle
End Function
