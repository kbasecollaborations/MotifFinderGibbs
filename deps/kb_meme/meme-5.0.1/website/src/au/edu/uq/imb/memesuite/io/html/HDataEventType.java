package au.edu.uq.imb.memesuite.io.html;

/**
 */
public enum HDataEventType {
  FILE_START,
  HIDDEN_FIELD,
  JSON_START_DATA,
  JSON_END_DATA,
  JSON_START_OBJECT,
  JSON_END_OBJECT,
  JSON_START_LIST,
  JSON_END_LIST,
  JSON_START_PROPERTY,
  JSON_END_PROPERTY,
  JSON_VALUE,
  JSON_ERROR,
  FILE_END,
}
