# APΩ macOS Background & Extension Surface Research

**Date:** 2026-07-31T21:48:09Z  
**Scope:** /Applications, /Users/andy/Applications, /Library, /Users/andy/Library, active processes, registered extensions, listening sockets  
**Mode:** READ_ONLY  
**Execution:** Automatic  

---

## 1. Executive Summary

This is a READ_ONLY scan of background runtime surfaces and extension surfaces on the local macOS host, performed under `APΩ_MACOS_BACKGROUND_EXTENSION_RESEARCH_SPECIFICATION` constraints. No mutations (install/uninstall/register/enable/disable/delete/modify) were performed.

Key findings:
- APOmegaEndpoint is now registered in the Endpoint Security extension surface and is `[activated waiting for user]`.
- Microsoft Defender (`UBF8T346G9`) holds an active Endpoint Security extension and a Network Extension, acting as a reference.
- Multiple applications embed nested background/extension surfaces (LoginItems, XPCServices, PlugIns, etc.).
- Listening sockets and `launchctl` user services are enumerated below.

---

## 2. System Extensions

```
3 extension(s)
--- com.apple.system_extension.network_extension (Go to 'System Settings > General > Login Items & Extensions > Network Extensions' to modify these system extension(s))
enabled	active	teamID	bundleID (version)	name	[state]
	*	UBF8T346G9	com.microsoft.wdav.netext (101.26062.0009/101.26062.0009)	Microsoft Defender Network Extension	[activated waiting for user]
--- com.apple.system_extension.endpoint_security (Go to 'System Settings > General > Login Items & Extensions > Endpoint Security Extensions' to modify these system extension(s))
enabled	active	teamID	bundleID (version)	name	[state]
*	*	UBF8T346G9	com.microsoft.wdav.epsext (101.26062.0009/101.26062.0009)	Microsoft Defender Endpoint Security Extension	[activated enabled]
	*	9ZM26YJTP4	com.nguyencuong.APOmegaOS.APOmegaEndpoint (1.0/1)	APOmegaEndpoint	[activated waiting for user]

```

## 3. Launchd User Domain

```
PID	Status	Label
-	0	com.apple.SafariHistoryServiceAgent
-	-9	com.apple.progressd
-	0	com.apple.enhancedloggingd
33888	-9	com.apple.cloudphotod
33460	-9	com.apple.MENotificationService
779	0	com.microsoft.wdav.tray
528	0	com.apple.Finder
12644	-9	com.apple.homed
33949	-9	com.apple.dataaccess.dataaccessd
-	0	com.apple.quicklook
-	0	com.apple.parentalcontrols.check
1173	0	application.com.tinfine.NotchBox.166429594.166429908
688	0	com.apple.mediaremoteagent
563	0	com.apple.FontWorker
34203	0	com.apple.bird
785	0	com.apple.amp.mediasharingd
-	-9	com.apple.knowledgeconstructiond
13207	-9	com.apple.inputanalyticsd
-	0	com.apple.familycontrols.useragent
-	0	com.apple.AssetCache.agent
33269	0	com.apple.GameController.gamecontrolleragentd
-	0	com.apple.universalaccessAuthWarn
-	0	com.apple.UserPictureSyncAgent
482	0	com.apple.nsurlsessiond
-	-9	com.apple.devicecheckd
32147	0	application.com.tinyspeck.slackmacgap.260852535.260869471
-	0	com.apple.syncservices.uihandler
29409	-9	com.apple.iconservices.iconservicesagent
2103	0	com.apple.diagnosticextensionsd
-	-9	com.apple.intelligenceplatformd
-	-9	com.apple.SafariBookmarksSyncAgent
-	0	com.apple.cmio.LaunchCMIOUserExtensionsAgent
34167	-9	com.apple.LinkedNotesUIService
-	-9	com.apple.ndoagent
536	0	com.apple.wallpaper.agent
-	0	com.apple.bookassetd
-	0	com.apple.ManagedClientAgent.agent
522	0	application.com.apple.Terminal.1152921500311914148.1152921500311914153
-	-9	com.apple.localizationswitcherd
-	0	com.apple.screensharing.agent
33369	-9	com.apple.commerce
69684	0	application.com.apple.MobileSMS.1152921500311888381.1152921500311888451
681	0	com.realvnc.vncagent.peruser
-	0	com.apple.AddressBook.SourceSync
-	-9	com.apple.installerauthagent
-	-9	com.apple.appleaccounttransparencyd
-	0	com.apple.languageassetd
-	0	com.apple.familynotificationd
33874	-9	com.apple.ManagedSettingsAgent
32481	-5	com.apple.photolibraryd
1149	0	application.com.postmanlabs.agent.mac.249480147.249480156
-	0	com.docker.helper
-	0	com.apple.xpc.otherbsd
-	0	com.apple.sysdiagnose_agent
-	-9	com.apple.ThreadCommissionerService
-	-9	com.apple.tipsd
-	0	com.pieces.os.launch
-	-9	com.apple.stickersd
-	-9	com.apple.bluetoothuserd
-	0	com.apple.timezoneupdates.tznotify
813	0	com.apple.TextInputMenuAgent
-	0	com.apple.bluetoothUIServer
-	0	com.axcontrol.canon.env
-	78	com.docker.mobile-relay
-	0	com.apple.accessibility.LiveTranscriptionAgent
-	0	com.apple.assistant_service
-	0	com.andy.cache-warmer
-	0	com.apple.MRTa
33370	-9	com.apple.CommCenter
12672	-9	com.apple.trustd.agent
-	0	com.apple.MailServiceAgent
-	0	com.apple.mdworker.mail
-	0	com.apple.appkit.xpc.ColorSampler
452	0	com.apple.cfprefsd.xpc.agent
-	0	com.apple.coreimportd
13471	-9	com.apple.CoreDevice.remotepairingd
33880	-9	com.apple.TrustedPeersHelper
-	0	com.apple.cvmsCompAgent3600_arm64_1
-	0	com.apple.DataDetectorsLocalSources
-	0	com.apple.unmountassistant.useragent
-	0	com.apple.facetimemessagestored
-	0	com.apple.AutoFillPanel
23974	-9	com.apple.peopled
-	0	com.apple.remo
```

## 4. Active Processes

```
  PID  PPID USER             COMM             ARGS
    1     0 root             /sbin/launchd    /sbin/launchd
  111     1 root             /usr/libexec/log /usr/libexec/logd
  113     1 root             /usr/libexec/Use /usr/libexec/UserEventAgent (System)
  115     1 root             /System/Library/ /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/FSEvents.framework/Versions/A/Support/fseventsd
  116     1 root             /System/Library/ /System/Library/PrivateFrameworks/MediaRemote.framework/Support/mediaremoted
  119     1 root             /usr/sbin/system /usr/sbin/systemstats --daemon
  123     1 root             /usr/libexec/con /usr/libexec/configd
  125     1 root             /System/Library/ /System/Library/CoreServices/powerd.bundle/powerd
  126     1 root             /usr/libexec/IOM /usr/libexec/IOMFB_bics_daemon
  130     1 root             /usr/libexec/rem /usr/libexec/remoted
  134     1 _corespeechd     /System/Library/ /System/Library/PrivateFrameworks/CoreSpeech.framework/corespeechd_system
  136     1 root             /usr/libexec/wat /usr/libexec/watchdogd
  140     1 root             /System/Library/ /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mds
  142     1 root             /usr/libexec/ker /usr/libexec/kernelmanagerd
  143     1 root             /usr/libexec/dis /usr/libexec/diskarbitrationd
  147     1 root             /usr/sbin/syslog /usr/sbin/syslogd
  149     1 root             /usr/libexec/the /usr/libexec/thermalmonitord
  150     1 root             /System/Library/ /System/Library/PrivateFrameworks/CoreDuetContext.framework/Resources/contextstored
  151     1 root             /usr/libexec/xpr /usr/libexec/xprotectd
  152     1 root             /usr/libexec/ope /usr/libexec/opendirectoryd
  153     1 root             /System/Library/ /System/Library/PrivateFrameworks/ApplePushService.framework/apsd
  154     1 root             /System/Library/ /System/Library/CoreServices/launchservicesd
  155     1 _timed           /usr/libexec/tim /usr/libexec/timed
  156     1 _usbmuxd         /System/Library/ /System/Library/PrivateFrameworks/MobileDevice.framework/Versions/A/Resources/usbmuxd -launchd
  157     1 root             /usr/sbin/securi /usr/sbin/securityd -i
  159     1 _locationd       /usr/libexec/loc /usr/libexec/locationd
  161     1 root             autofsd          autofsd
  162     1 root             /usr/libexec/das /usr/libexec/dasd
  163     1 root             /System/Library/ /System/Library/PrivateFrameworks/Heimdal.framework/Helpers/kdc
  164     1 root             /usr/libexec/cor /usr/libexec/corerepaird
  166     1 _distnote        /usr/sbin/distno /usr/sbin/distnoted daemon
  168     1 root             /usr/libexec/Per /usr/libexec/PerfPowerServices
  170     1 root             /System/Library/ /System/Library/CoreServices/logind
  171     1 root             /System/Library/ /System/Library/PrivateFrameworks/
```

## 5. Listening Sockets

```
COMMAND     PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
rapportd    488 andy   10u  IPv4 0xf28d8fabcb7d9cee      0t0  TCP *:49157 (LISTEN)
rapportd    488 andy   11u  IPv6 0xb6fff1916fe40050      0t0  TCP *:49157 (LISTEN)
rapportd    488 andy   18u  IPv6 0x6aebeeb3f18cd13a      0t0  TCP *:60536 (LISTEN)
rapportd    488 andy   24u  IPv6 0x22aa0a82776c1cc7      0t0  TCP *:60537 (LISTEN)
ControlCe   526 andy    9u  IPv4 0x84722c2c1edc5372      0t0  TCP *:7000 (LISTEN)
ControlCe   526 andy   10u  IPv6 0x74b23959894168f6      0t0  TCP *:7000 (LISTEN)
ControlCe   526 andy   11u  IPv4 0x3f843f0a8aa3b680      0t0  TCP *:5000 (LISTEN)
ControlCe   526 andy   12u  IPv6 0x17d436e986f79eb5      0t0  TCP *:5000 (LISTEN)
ARDAgent    562 andy   10u  IPv6 0x3cda9ef361fca73b      0t0  TCP *:3283 (LISTEN)
mediashar   785 andy    6u  IPv4  0xd9e6f3d31d857ef      0t0  TCP *:3689 (LISTEN)
mediashar   785 andy    7u  IPv6  0xe8fd73f2f8bdd81      0t0  TCP *:3689 (LISTEN)
redis-ser   787 andy    6u  IPv4 0x74d6f83e9544f29e      0t0  TCP 127.0.0.1:6379 (LISTEN)
redis-ser   787 andy    7u  IPv6 0xcdebe2012b50083b      0t0  TCP [::1]:6379 (LISTEN)
Python      809 andy    4u  IPv4 0x7c5bd05225a7f5f8      0t0  TCP 127.0.0.1:50520 (LISTEN)
Ollama      831 andy    4u  IPv4 0x3079addbe5853d17      0t0  TCP 127.0.0.1:49196 (LISTEN)
ollama      864 andy    3u  IPv6 0xaf6991367d452aa3      0t0  TCP *:11434 (LISTEN)
Postman    1149 andy   33u  IPv4 0x68d944039a1a559f      0t0  TCP 127.0.0.1:10533 (LISTEN)
Electron   1155 andy   46u  IPv4 0xeafc96140408334b      0t0  TCP 127.0.0.1:51017 (LISTEN)
Electron   1155 andy   48u  IPv4 0xd11ce0db56a2960d      0t0  TCP 127.0.0.1:51018 (LISTEN)
Parallels  1161 andy    8u  IPv4 0x785e5c92a3a93746      0t0  TCP 127.0.0.1:57889 (LISTEN)
Parallels  1161 andy   11u  IPv6 0x26a60945af92135f      0t0  TCP [::1]:57889 (LISTEN)
LM\x20Stu  1169 andy   76u  IPv4 0x2f5a374c9b00b2c6      0t0  TCP 127.0.0.1:41343 (LISTEN)
LM\x20Stu  1169 andy   78u  IPv4 0x1a5c7
```

## 6. PlugInKit Extensions

```
+    com.my.mail.share-extension(15.11.0)
     com.apple.WatchFaceAlert.ThumbnailExtension(1.0)
     com.apple.priml.PFLMLHostPlugins.SiriAutoEvalPlugin((null))
     com.apple.FaceTime.FaceTimeNotificationExtension((null))
     com.apple.ScreenSaver.Ventura(1.0)
+    com.apple.MarkupUI.MarkupPhotoExtension(1.0)
     com.readdle.ReaddleDocsIPad.DocumentsPushNotificationContentExtension(8.20.4)
     com.apple.MediaExtensions-Settings((null))
     com.apple.CryptoTokenKit.pivtoken(1.0)
     com.tinfine.NotchBox.SafariEx(1.1.69)
     net.neuro9.lmmini.LMWidgetExtension(1.8.8)
     com.apple.iCal.FaceTimeExtension(1)
     com.ip18.Clone-in-VS-Code.Extension(1.5.0)
     com.apple.games.ChallengesMessageExtension(1.0)
+    com.crossforward.WidgetSmith.SharePhoto(8.4)
     com.microsoft.Microsoft-Rewards-for-Safari.Extension(1.0.0)
     com.apple.HomeKitEvents.HomeKitEventsDiagnosticExtension(1)
     tomoyaonishi.SafariQRCode.Extension(2.0.0)
     com.apple.diagnosticextensions.osx.spotlight(1.0)
     com.apple.diagnosticextensions.osx.timemachine(1.0)
     com.apple.DiagnosticExtensions.sysdiagnose(1.0)
     com.apple.Safari.SafariLinkExtension(1)
     com.apple.poirot.MessagesAnalyticsWorker((null))
+    com.quantumquinn.TextToolset.TextToolsetXcodeExtension(1.4.1)
     com.apple.siri.OnDeviceAnalytics.SpeakerIdSamplingExtension((null))
     dk.andersborum.ftp.widget(2026.31)
+    net.homeunix.hio.app.LanguageTranslator.LanguageTranslatorExtension(1.2)
     com.apple.controls.screenshot(1.0)
+    com.lukilabs.lukiapp.CraftShareExtension(3.5.3)
     com.gsm.customer.NotificationService(5.5.1)
+    com.my.mail.mail-to-self(15.11.0)
     com.mr-brightside.myParcel.ParcelWidget(8.6.3)
     com.apple.extensionkit.AppExtensionManagement(1)
     com.apple.systempreferences.KeyboardSettingsExtension((null))
+    ru.keepcoder.Telegram.TelegramShare(12.9)
     com.apple.systempreferences.DisplaysSettingsIntents(1.0)
     com.ideasoncanvas.mindnode.quicklook(2026.4.1)
     com.apple
```

## 7. LaunchAgents / LaunchDaemons

### /Library/LaunchAgents
- `com.google.keystone.xpcservice.plist`
- `com.teamviewer.teamviewer_desktop.plist`
- `com.google.keystone.agent.plist`
- `com.microsoft.SyncReporter.plist`
- `com.teamviewer.teamviewer.plist`
- `com.oracle.java.Java-Updater.plist`
- `com.realvnc.vncagent.prelogin.plist`
- `org.chromium.chromoting.plist`
- `com.microsoft.OneDriveStandaloneUpdater.plist`
- `com.microsoft.wdav.tray.plist`
- `com.realvnc.vncagent.peruser.plist`
- `com.microsoft.update.agent.plist`

### /Library/LaunchDaemons
- `com.microsoft.OneDriveStandaloneUpdaterDaemon.plist`
- `com.teamviewer.UninstallerWatcher.plist`
- `com.docker.vmnetd.plist`
- `com.microsoft.OneDriveUpdaterDaemon.plist`
- `com.docker.socket.plist`
- `com.google.GoogleUpdater.wake.system.plist`
- `com.microsoft.fresno.plist`
- `com.parallels.desktop.launchdaemon.plist`
- `com.microsoft.fresno.uninstall.plist`
- `com.microsoft.wdav.tracer_install_monitor.plist`
- `com.google.keystone.daemon.plist`
- `com.microsoft.dlp.install_monitor.plist`
- `com.microsoft.wdav.dlp_processor_install_monitor.plist`
- `com.teamviewer.UninstallerHelper.plist`
- `com.teamviewer.Helper.plist`
- `com.teamviewer.teamviewer_service.plist`
- `org.chromium.chromoting.broker.plist`
- `com.microsoft.office.licensingV2.helper.plist`
- `com.realvnc.vncserver.plist`
- `com.microsoft.autoupdate.helper.plist`

### /Users/andy/Library/LaunchAgents
- `com.andy.cache-warmer.plist`
- `com.aios.mission.router.plist`
- `com.google.keystone.xpcservice.plist`
- `com.dropbox.dropboxmacupdate.xpcservice.plist`
- `com.microsoft.msbwupdater.plist`
- `testcontainers.desktop.plist`
- `com.hyperai.telemetry.router.loop.plist`
- `com.google.keystone.agent.plist`
- `com.andy.apo.gam-memory-guard.plist`
- `com.apomega.meshctl.probe.plist`
- `com.grammarly.ProjectLlama.Uninstaller.plist`
- `com.microsoft.msbwapp.plist`
- `com.hyperai.finalai-openai-proxy.plist`
- `com.docker.mobile-relay.plist`
- `com.hyperai.orchestrator.plist`
- `com.hyperai.connector.watchdog.plist`
- `com.hyperai.escalation.plist`
- `com.pieces.os.launch.plist`
- `homebrew.mxcl.code-server.plist`
- `com.hyperai.clawbot.metrics.plist`
- `com.vietnamese.ai.symphony.autolauncher.plist`
- `com.axcontrol.canon.env.plist`
- `com.dropbox.DropboxUpdater.wake.plist`
- `ai.openclaw.gateway.plist`
- `com.hyperai.nightwatch.plist`
- `com.hyperai.os.master.plist`
- `homebrew.mxcl.redis.plist`
- `com.hyperai.registry.dashboard.plist`
- `com.andy.identity-guard.plist`
- `com.grammarly.ProjectLlama.UpdateService.plist`
- ... and 10 more

## 8. Applications with Background / Extension Surfaces

**Count:** 2 apps with nested surfaces.

### Swiftify for Xcode.app
- Path: `/Applications/Swiftify for Xcode.app`
- Bundle ID: `com.Swiftify.Xcode`
- **LoginItems:** `Swiftify Service.app`

### Todoist.app
- Path: `/Applications/Todoist.app`
- Bundle ID: `com.todoist.mac.Todoist`
- **LoginItems:** `Todoist Login Helper.app`

---

## 9. Capability & Authority Graph

| Item | State | Capability | Reusability for OmegaOS |
|------|-------|------------|------------------------|
| Microsoft Defender ES | active enabled | `com.apple.developer.endpoint-security.client` | REFERENCE_ONLY (third-party, cannot absorb) |
| APOmegaEndpoint | activated waiting for user | `com.apple.developer.endpoint-security.client` | OMEGA_LINEAGE (own build) |
| APOmegaStateDaemon | embedded LaunchDaemon | XPC / signed Mach | OMEGA_LINEAGE |
| APOmegaOS.app | /Applications, signed | system-extension install, sandbox, XPC | OMEGA_LINEAGE |

## 10. Evidence Levels Applied

- L0_VISIBLE: apps, `systemextensionsctl`, `launchctl` output.
- L1_REGISTERED: launchd, `systemextensionsctl`, LaunchAgent plist files.
- L2_PHYSICAL: bundle paths, `Info.plist`, executables.
- L3_AUTHORIZED: `codesign -dvv` TeamIdentifier and entitlements (performed selectively on APΩ and reference).
- L4_RUNTIME: `ps`, `lsof`, `systemextensionsctl` state.
- L5_FUNCTIONAL: APΩ endpoint reached `[activated waiting for user]`; full functional probe blocked by user-consent gate.

## 11. External Boundary & Next Action

Per `OS_HARDWARE_REALITY_SPECIFICATION`, the current APΩ endpoint is an optional privileged sensor. Its absence does not block OmegaOS core execution. The next single action is:

1. User opens **System Settings → General → Login Items & Extensions → Endpoint Security Extensions**.
2. User clicks **Allow** for `APOmegaEndpoint`.
3. Re-run `systemextensionsctl list` to confirm `[activated enabled]`.
4. Re-probe the EndpointSecurity `ES_NEW_CLIENT_RESULT_SUCCESS` callback.

## 12. Findings

- **F1** APOmegaEndpoint is physically signed, embedded, installed in `/Applications`, and registered with the OS.
- **F2** The only remaining local gate is macOS user consent.
- **F3** `xcodegen` entitlement overwrite issue is fixed by moving entitlement/Info.plist properties into `project.yml`.
- **F4** CloudKit cache regrows rapidly under iCloud sync and causes disk pressure during build/test cycles.
- **F5** No other background items depend on APOmegaEndpoint; its `APOmegaStateDaemon` is self-contained and embedded.

---

**Orch mode:** READ_ONLY scan → evidence collection → capability/authority graph → external boundary report.  
**Agent chain status:** closed on research surface scan; open on macOS user consent.
