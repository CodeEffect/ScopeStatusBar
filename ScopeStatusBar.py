# coding=utf-8
import sublime_plugin
import sublime


class ScopeStatusBarCommand(sublime_plugin.TextCommand):

    enabled = False

    def run(self, edit, update=False, toggle=False):
        if toggle is True:
            self.enabled = False if self.enabled else True
            if self.enabled:
                if not hasattr(self, "output_view"):
                    self.output_view = sublime.active_window().create_output_panel("scope")
                    self.output_view.settings().set("word_wrap", True)
                    self.output_view.settings().set("line_numbers", False)
                    self.output_view.settings().set("gutter", False)
                    self.output_view.settings().set("scroll_past_end", False)
                    self.output_view.settings().set("font_size", 14)
                    self.output_view.settings().set("draw_centered", True)
                    self.output_view.set_name("SCOPER")
                    sublime.active_window().create_output_panel("scope")
                sublime.active_window().run_command(
                    "show_panel",
                    {"panel": "output.scope"}
                )
                sublime.active_window().run_command(
                    "scope_status_bar",
                    {"update": True}
                )
            else:
                sublime.active_window().run_command("hide_panel")
        elif self.enabled:
            # Sometimes sublime_api.view_scope_name throws its toys:
            #   UnicodeDecodeError: 'utf-8' codec can't decode bytes in position 18-19: invalid continuation byte
            try:
                scopes = sublime.active_window().active_view().scope_name(
                    sublime.active_window().active_view().sel()[0].a
                ).strip()
            except:
                scopes = ""
            print(scopes, sublime.active_window().active_view().name())
            # view.set_status("SSB", "[%s]" % (
            #     scopes
            # ))
            self.output_view.set_read_only(False)
            self.output_view.replace(
                edit,
                sublime.Region(0, self.output_view.size() + 1),
                scopes
            )
            self.output_view.set_read_only(True)


class ScopeStatusBar(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        if view.name() != "SCOPER":
            sublime.active_window().run_command(
                "scope_status_bar",
                {"update": True}
            )
