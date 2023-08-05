#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ConfigParser
import datetime
import optparse
import os
import pytz
import sys
import wx
import wx.lib.masked

"""Show timezones in a window."""

__author__ = 'Scott Kirkwood (scott+keymon@forusers.com)'
__version__ = '0.2.0'

class MyZonesApp(wx.App):
    def init_vars(self):
        self.config = self.LoadConfig({
          'show_seconds' : True,
          'edit_names' : False,
          'edit_tz' : False,
          'update_time' : True,
        })
        self.FixEmptyTimezones()

    def OnInit(self):
        self.init_vars()
        self.dialog = wx.Frame(None, -1, "Time Zones")
        self.dialog.Show(True)
        self.SetTopWindow(self.dialog)

        self.CurrentTime()
        self.SetupControls(self.dialog)
        self.OnTimer(None)
        wx.EVT_ACTIVATE(self, self.OnActivate)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.StartTimer()
        self.dialog.Fit()
        return True

    def LoadConfig(self, config):
        """
        returns a dictionary with key's of the form
        <section>.<option> and the values
        From: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/65334
        """
        class MyConfigParser(ConfigParser.SafeConfigParser):
          def optionxform(self, option):
            """ I want to maintain the case of the options """
            return str(option)

        config = config.copy()
        cp = MyConfigParser()
        cp.read([os.path.expanduser('~/.myzones.ini'),
                os.path.expanduser('~/myzones.ini'), 'myzones.ini'])
        config['timezones'] = []
        nIndex = 0
        for sec in cp.sections():
            name = sec.lower()
            for opt, value in cp.items(sec):
                if name == 'config':
                    opt = opt.lower()
                    if opt in ['show_seconds', 'edit_tz']:
                        config[opt] = cp.getboolean(sec, opt)

                elif name == 'timezones':
                    tz_infos = value.split('|')
                    if len(tz_infos) == 1:
                        value = tz_infos[0]
                        nIndex += 1
                    else:
                        nIndex = int(tz_infos[0])
                        value = tz_infos[1]
                    config['timezones'].append((nIndex,
                            {'title' : opt, 'tz' :value}))

        config['timezones'].sort()
        return config

    def FixEmptyTimezones(self):
      if len(self.config['timezones' ]) == 0:
        self.config['timezones'] += [
          (1, dict( title='PST', tz='US/Pacific')),
          (2, dict(title='EST', tz='US/Eastern')),
          (3, dict(title='BRST', tz='Brazil/East')),
        ]

    def SetupControls(self, dialog):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        h = 28
        for  index, timezone in self.config['timezones']:
            hsizer.Add(self.AddTimeControls(timezone, dialog, h), 0)
        dialog.SetSizer(hsizer)

        #self.sb = dialog.CreateStatusBar()
        for index, timezone in self.config['timezones']:
            self.Bind(wx.EVT_SPIN, self.OnSpinChange, timezone['spinctl'])

    def StartTimer(self):
        self.timer = wx.Timer(self)
        self.timer.Start(1000)

    def AddTimeControls(self,timezone, dialog, h):
        vsizer = wx.BoxSizer(wx.VERTICAL)

        textCtrl = wx.StaticText(dialog, -1, timezone['title'],  style=wx.ALIGN_CENTER)
        vsizer.Add(textCtrl, 0, wx.EXPAND)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        timezone['spinctl'] = wx.SpinButton(dialog, -1, wx.DefaultPosition,  (-1, h),
            wx.SP_VERTICAL)
        timeCtl = wx.lib.masked.TimeCtrl(
            dialog, -1, name=timezone['title'], fmt24hr=True,
            display_seconds = self.config['show_seconds'],
            spinButton = timezone['spinctl'])
        timezone['timectl'] = timeCtl
        hsizer.Add(timeCtl, 0, wx.ALL, 2)
        hsizer.Add(timezone['spinctl'], 0, wx.ALL, 2)
        vsizer.Add(hsizer, 0, wx.ALIGN_CENTER )

        #~ cb = wx.ComboBox(dialog, -1, timezone['tz'],
                #~ choices=pytz.common_timezones, style=wx.CB_DROPDOWN)
        cb = wx.StaticText(dialog, 1, timezone['tz'], style=wx.ALIGN_CENTER)
        vsizer.Add(cb, 0, wx.EXPAND)

        return vsizer

    def CurrentTime(self):
        utc_dt = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self.UpdateAllTimes(utc_dt)

    def UpdateAllTimes(self, utc_dt):
        for index, zone in self.config['timezones']:
            tzinf = pytz.timezone(zone['tz'])
            loc_dt = utc_dt.astimezone(tzinf)
            zone['loc_dt'] = loc_dt
            zone['timenow'] = loc_dt.strftime('%H:%M:%S')
            zone['utcoffset'] = (tzinf.utcoffset(0).days * 24) + tzinf.utcoffset(0).seconds / (60.0 * 60)

    def FindBySpinCtrl(self, spinctl):
        for index, zone in self.config['timezones']:
            if zone['spinctl'] == spinctl:
              return zone
        return None

    def OnSpinChange(self, event):
        self.timer.Stop()
        self.config['update_time'] = False

        self.last_spin_changed = self.dialog.FindWindowById(event.GetId())
        zone = self.FindBySpinCtrl(self.last_spin_changed)
        timectrl = zone['timectl']
        times = timectrl.GetValue().split(':')
        zone['loc_dt'] = zone['loc_dt'].replace(hour = int(times[0]), minute=int(times[1]))
        if len(times) > 2:
            zone['loc_dt'] = zone['loc_dt'].replace(second=int(times[2]))

        utc_dt = zone['loc_dt'].astimezone(pytz.utc)
        self.UpdateAllTimes(utc_dt)
        self.UpdateTimeControls()

    def OnTimer(self, unused_event):
        self.CurrentTime()
        self.UpdateTimeControls()

    def UpdateTimeControls(self):
        for index, zone in self.config['timezones']:
          now = wx.DateTime()
          dt = zone['loc_dt']
          now.Set(dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
          zone['timectl'].SetValue(now)

    def OnActivate(self, event):
        event.Skip()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyZonesApp(None, -1, 'My Zones')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

def RunWxApp():
    app = MyZonesApp(0)
    app.MainLoop()

def show_version():
    """Show the version number and author, used by help2man."""
    print 'Keymon version %s.' % __version__
    print 'Written by %s' % __author__

def parse_command_line():
    parser = optparse.OptionParser()
    parser.add_option('-v', '--version', dest='version', action='store_true',
                      help='Show version information and exit.')
    parser.add_option('-l', '--list', help="List all common time zones",
        action="store_true", dest="blist")

    (options, args) = parser.parse_args()

    if options.version:
      show_version()
      sys.exit(0)
    elif options.blist:
        for tz in pytz.common_timezones:
            print "%s" % (tz)
        sys.exit(0)

    RunWxApp()

if __name__ == '__main__':
    parse_command_line()

