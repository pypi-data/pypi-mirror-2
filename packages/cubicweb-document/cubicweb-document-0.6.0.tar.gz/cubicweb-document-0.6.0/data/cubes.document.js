// This contains template-specific javascript

function switch_branch(this_id) {
  remoteExec('set_cookie', 'branch_scope', jQuery('#'+this_id).val());
  document.location=document.location;
}

function DJoin(count) {
  // This allows to call back a function when a set of deferreds
  // is completely done. You must provide the expected number of deferreds.
  // Ex:
  // var d = DJoin(2);
  // d.register(reloadComponent('foo'));
  // d.register(reloadComponent('bar'));
  // d.add_callback(function () { document.location.href = 'www.perdu.com' });
  this.__init__(this, count);
}

jQuery.extend(DJoin.prototype, {
  __init__: function(self, count) {
    self._count = count;
    self._cb = null;
  },

  _notifier: function(self) {
    return function () {
      self._count = self._count - 1;
      if ((self._count < 1) & !(self._cb === null)) {
        self._cb();
      }
    };
  },

  register: function(deferred) {
    // no bound method in JS, hence the closure
    // cf. _notifier
    deferred.addCallback(this._notifier(this));
    deferred.addErrback(this._notifier(this));
  },

  add_callback: function(cb) {
    if (this._count) {
      this._cb = cb;
    } else {
      cb();
   }
  }
});

function update_edition_status(vfrql, usereid, will_edit) {
  remoteExec('update_edition_status', vfrql, usereid, will_edit);
  var djoin = new DJoin(3);
  djoin.register(reloadComponent('edit_box', vfrql, 'boxes', 'edit_box'));
  djoin.register(reloadBox('user_worklist_box'));
  djoin.register(reloadComponent('edition_status', vfrql, 'views', 'edition-status'));
  return djoin;
}
