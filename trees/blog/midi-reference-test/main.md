---
title: 对 Moonbit Midi 进行 Reference Test
collect: true
author: [Elevonic611](https://github.com/HarryLiGameTech)
taxon: Blog
date: 2025-10-31
---

目前 Moonbit 语言的 Midi 编解码工具已逐步实现基本功能，为确保其解码测试样例正确有效，我们编写了这套逻辑，以验证 Moonbit 解码结果（测试样例）与现有的 midi 解码工具（mido）的输出是否等价。

毕竟，只有确保测试集可信，才能指导 Moonbit Midi 的继续开发。

(Moonbit Midi 具体实现详见：https://github.com/CAIMEOX/midi，
此文不做额外赘述)

## 基本思路/流程
1. 选择一首复杂度合适的 mid 文件（此次以 star_wars 作为样例，详见 Moonbit Midi 库）
2. 使用 Python mido 以及 Moonbit midi 分别进行解码，获取 mid 文件中的所有 event 内容
3. 对两边解码出的内容整理成统一格式（确保无信息丢失）
4. 对整理后的内容进行比较，如果完全相等（忽略 system-specific 的 event，仅关注标准协议明确定义的内容），则代表解码正确

这是整个过程的代码：

```python
def ref_test(mbt_parsed_text, file_name):
    from_py = ""
    from_mbt = to_mido_format(mbt_parsed_text)
    trusted_parser.read_midi_file(file_name)
    with open('from_py.txt', 'r') as f:
        from_py = f.read()

    compare(from_py, from_mbt)
```


## 具体实现

首先使用 python mido 建立一个**可信的 (trusted)** 解码器。全部使用 mido 库提供的 API，不自定义解析逻辑：

```python
def read_midi_file(filename):
    """
    Read and parse a MIDI file from disk.
    
    Args:
        filename (str): Path to the MIDI file
    
    Returns:
        MidiFile: Parsed MIDI file object
        list: List of all messages from all tracks
    """
    try:
        original_stdout = sys.stdout

        # Load the MIDI file using mido
        midi_file = MidiFile(filename)
        
        messages = []
        
        # Store the parsed text in a file
        with open('from_py.txt', 'w') as f:
            sys.stdout = f
            # Extract all messages from all tracks
            for i, track in enumerate(midi_file.tracks):
                for msg in track:
                    messages.append(msg)
                    print(f"{msg}")
                if i < len(midi_file.tracks) - 1:
                    print("------")

        sys.stdout = original_stdout

        return midi_file, messages
        
    except Exception as e:
        print(f"Error reading MIDI file: {e}")
        return None, []
```

由于 mido 和 Moonbit Midi 解码后的文字格式不完全一样，需要在 compare 之前，将 Moonbit 解码后得到的文字进行如下操作：

```python
def to_mido_format(mbt_parsed_text):
    """
    Convert MBT parsed text to Mido-compatible format
    
    Args:
        mbt_parsed_text (str): The parsed text from MBT format
        
    Returns:
        str: Mido-compatible formatted text
    """
    lines = mbt_parsed_text.split('\n')
    processed_lines = []
    
    for line in lines:
        if not line.strip():
            processed_lines.append(line)
            continue
            
        # Apply all transformations in sequence
        transformed_line = line
        
        # 1. Replace fixed texts to meet mido format
        transformed_line = re.sub(r'NoteOn', 'note_on', transformed_line)
        transformed_line = re.sub(r'NoteOff', 'note_off', transformed_line)
        transformed_line = re.sub(r'SysEx', 'sysex', transformed_line)
        transformed_line = re.sub(r'ProgramChange', 'program_change', transformed_line)
        transformed_line = re.sub(r'ControlChange', 'control_change', transformed_line)
        transformed_line = re.sub(r'SysEx', 'sysex', transformed_line)

        transformed_line = re.sub(r'ctrl', 'control', transformed_line)
        transformed_line = re.sub(r'vel', 'velocity', transformed_line)
        transformed_line = re.sub(r'val', 'value', transformed_line)
        
        # 2. Replace [ch X] with channel=X
        transformed_line = re.sub(r'\[ch (\d+)\]', r' channel=\1 ', transformed_line)
        
        # 3. Remove (XX) from note=XX(XX) patterns
        transformed_line = re.sub(r'note=(\d+)\([^)]+\)', r'note=\1', transformed_line)
        
        # 4. Move time=XX to the end of the line
        time_match = re.search(r'\[(\d+)\]', transformed_line)
        if time_match:
            time_value = f"time={time_match.group(1)}"
            # Remove the time bracket
            transformed_line = re.sub(r'\[\d+\]', '', transformed_line)
            # Add time to the end
            transformed_line = transformed_line.strip() + ' ' + time_value

        # 5. Remove instrument description
        transformed_line = re.sub(r'(program=\d+):.*?(?=time=|$)', r'\1 ', transformed_line)

        # 6. Convert SysEx format to Mido-compatible format
        if transformed_line.startswith('sysex'):
            # Remove 'len=XX' part
            transformed_line = re.sub(r'len=\d+', '', transformed_line)
            # Convert hex array to tuple format
            transformed_line = re.sub(r'\[([0-9A-Fa-f ]+)\]', 
                                    lambda m: f"data=({','.join(m.group(1).split())})", 
                                    transformed_line)
            # Convert to lowercase
            transformed_line = transformed_line.lower()
            # Clean up any extra spaces
            transformed_line = re.sub(r'\s+', ' ', transformed_line).strip()
        
        # 7. Clean up any extra spaces
        transformed_line = re.sub(r'\s+', ' ', transformed_line).strip()
        
        processed_lines.append(transformed_line)
    
    return '\n'.join(processed_lines)
```

最后使用 compare() 函数比较格式统一后的解码文本，如返回 True，则代表 moonbit midi 解码出的内容正确：

```python
def compare(from_py, from_mbt):
    # Split both strings into lines
    py_lines = from_py.splitlines()
    mbt_lines = from_mbt.splitlines()
    
    # Find the maximum number of lines to compare
    max_lines = max(len(py_lines), len(mbt_lines))
    
    differences_found = False
    
    for i in range(max_lines):
        # Get lines from both sources (or empty string if line doesn't exist)
        py_line = py_lines[i] if i < len(py_lines) else ""
        mbt_line = mbt_lines[i] if i < len(mbt_lines) else ""
        
        # Strip and normalize whitespace for comparison
        py_stripped = ' '.join(py_line.split())
        mbt_stripped = ' '.join(mbt_line.split())
        
        # Compare the normalized lines
        if py_stripped != mbt_stripped:
            return False
    
    # No difference found after iterating thru everything
    return True
```


## 后期目标

目前 reference test 仍需要大量手动操作，需要额外存储 Moonbit 解码文本。当 Moonbit 方测试样例变更时，重新确认其有效性会变得比较麻烦。

因此我们设想：可否让 Moonbit 自动执行我编写的 Python 代码，并进行跨语言数据通信？

目前看来，Kaida-Amethyst 主导开发的 python.mbt 库 (https://github.com/moonbitlang/python.mbt) 或许可以帮助我们实现目标。根据其给出的技术文档，写出如下 Moonbit 代码：

```moonbit
typealias @python.(PyString, PyTuple)

test "reference_test" {
  ///////////////////////////////////////////////////////////////
  // Equal to: from verifier import ref_test
  guard @python.pyimport("verifier") is Some(verifier)
  guard verifier.get_attr("ref_text") is Some(PyCallable(verify))
  ///////////////////////////////////////////////////////////////

  let verifiee : String = (
      #|format=1
      #|division=384
      #|tracks:10
      #|TimeSignature[0] numerator=3 denominator=4 clocks_per_tick=24 thirty_seconds_per_quarter=8
      #|Tempo[0] microseconds=480000 (125 BPM)
      #|TimeSignature[1152] numerator=4 denominator=4 clocks_per_tick=24 thirty_seconds_per_quarter=8
      #|Meta[19968] type=47 len=0 []
      #|------
      #|Meta[0] type=3 len=10 [70 73 78 71 69 82 68 66 65 83]
      #|ControlChange[424][ch 1] ctrl=121 val=0
      
      ///////////////////////////
      // 具体内容省略，有几千行 ///
      ///////////////////////////

      #|Meta[6144] type=47 len=0 []
  )

  //////////////////////////////////////////////////////////////
  // Equal to: is_identical = ref_test(verifiee, "star_wars.mid")
  let args = PyTuple::new(2)
  args
  ..set(0, PyString::from(verifiee))
  ..set(1, PyString::from("star_wars.mid"));
  guard verify.invoke(args~) is Some(is_identical) 
  ///////////////////////////////////////////////////////////////


  // Convert to Moonbit type
  guard is_identical is PyBool(is_identical)

  inspect(is_identical, content="True")
}
```

不过，这份代码**还无法正常运行**，因为 python.mbt 貌似没有识别我编写的 python 文件。目前 Kaida-Amethyst 还未在文档中提及 Moonbit 引入自定义 python 文件的方法，我已在对应 repo 中的 issue 提出修改 documentation 的建议和请求。

待作者完善技术文档后，我将会更新此篇文章，提供可运行的方案。