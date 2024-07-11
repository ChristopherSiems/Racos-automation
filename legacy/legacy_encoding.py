def config_to_hatch(config : str, style : str) -> str:
  '''
  returns the hatch pattern for the inputted config
  :param config: the config string of values making up the config
  :param style: selects the mapping of configs to hatches
  :returns: the hatch pattern for the inputted config
  '''
  if style == 'delay':
    if re.match(ZERO_CONFIG_PATTERN, config): return ''
    if re.match(ONE_CONFIG_PATTERN, config): return '..'
    if re.match(FIVE_CONFIG_PATTERN, config): return '++'
    if re.match(TEN_CONFIG_PATTERN, config): return 'xx'
  if style == 'packet_loss':
    if re.match(POINT_ONE_CONFIG_PATTERN, config): return '..'
    if re.match(POINT_FIVE_CONFIG_PATTERN, config): return '++'
    if re.match(ONE_CONFIG_PATTERN, config): return 'xx'

def config_to_line_style(config : str) -> str:
  '''
  returns the line style pattern for the inputted config
  :param config: the config string of values making up the config
  :returns: the line style pattern for the inputted config
  '''
  if re.match(POINT_ONE_CONFIG_PATTERN, config): return ':'
  if re.match(POINT_FIVE_CONFIG_PATTERN, config): return '--'
  if re.match(ONE_CONFIG_PATTERN, config): return '-.'

def config_to_marker(config : str) -> str:
  '''
  returns the marker pattern for the inputted config
  :param config: the config string of values making up the config
  :returns: the marker pattern for the inputted config
  '''
  if re.match(POINT_ONE_CONFIG_PATTERN, config): return 'o'
  if re.match(POINT_FIVE_CONFIG_PATTERN, config): return '^'
  if re.match(ONE_CONFIG_PATTERN, config): return 's'

def config_to_offset(config : str, style : str) -> float:
  '''
  returns the offset pattern for the inputted config
  :param config: the config string of values making up the config
  :param style: selects the mapping of configs to hatches
  :returns: the offset value for the inputted config
  '''
  if style == 'delay':
    if re.match(ZERO_CONFIG_PATTERN, config): return -.36
    if re.match(ONE_CONFIG_PATTERN, config): return -.12
    if re.match(FIVE_CONFIG_PATTERN, config): return .12
    if re.match(TEN_CONFIG_PATTERN, config): return .36
  if style == 'packet_loss':
    if re.match(POINT_ONE_CONFIG_PATTERN, config): return -.32
    if re.match(POINT_FIVE_CONFIG_PATTERN, config): return 0
    if re.match(ONE_CONFIG_PATTERN, config): return .32

ZERO_CONFIG_PATTERN : re.Pattern = re.compile(r'^0(_0)*$')
POINT_ONE_CONFIG_PATTERN : re.Pattern = re.compile(r'^0\.1(_0\.1)*$')
POINT_FIVE_CONFIG_PATTERN : re.Pattern = re.compile(r'^0\.5(_0\.5)*$')
ONE_CONFIG_PATTERN : re.Pattern = re.compile(r'^1(_1)*$')
FIVE_CONFIG_PATTERN : re.Pattern = re.compile(r'^5(_5)*$')
TEN_CONFIG_PATTERN : re.Pattern = re.compile(r'^10(_10)*$')