var EXPORTED_SYMBOLS = ["MozmillError"];

function MozmillError(err, message, fileName, lineNumber) {
  this.stack = err.stack;
  this.message = message || err.message;
  this.name = err.name;
  this.fileName = fileName || err.fileName;
  this.lineNumber = lineNumber || err.lineNumber;
};
MozmillError.prototype = new Error();
MozmillError.prototype.constructor = MozmillError;
MozmillError.prototype.name = 'MozmillError';
