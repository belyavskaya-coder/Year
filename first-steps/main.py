# main.py — Тур-Счётчик с датой, очисткой и историей
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from datetime import datetime
import json
import os

Window.size = (360, 640)
import os
from kivy.utils import platform

# Определяем, где запущено приложение
if platform == "android":
    # На телефоне — в защищённую папку приложения
    DATA_DIR = "/storage/emulated/0/Android/data/org.tourcounter/files"
else:
    # На компьютере — в домашнюю папку пользователя
    DATA_DIR = os.path.expanduser("~/.tourcounter")

os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, "data.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "current": {"date": "", "collected": 0, "items": []},
        "history": []  # список: [{"date":"04.11", "total":63200, "text":"..."}, ...]
    }

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

class TourCounterApp(App):
    def build(self):
        self.data = load_data()
        self.current = self.data["current"]
        self.history = self.data.get("history", [])

        layout = BoxLayout(orientation="vertical", padding=10, spacing=8)

        # === Дата и собрано ===
        date_collected = BoxLayout(size_hint_y=None, height=45, spacing=8)
        self.date_input = TextInput(
            text=self.current.get("date", ""),
            hint_text="Дата (напр. 04–07.11)",
            multiline=False,
            size_hint_x=0.5
        )
        self.collected_input = TextInput(
            text=str(self.current.get("collected", 0)),
            hint_text="Собрано (₽)",
            input_filter="int",
            multiline=False,
            size_hint_x=0.5
        )
        self.date_input.bind(text=self.on_data_change)
        self.collected_input.bind(text=self.on_data_change)
        date_collected.add_widget(self.date_input)
        date_collected.add_widget(self.collected_input)
        layout.add_widget(date_collected)

        # === Список строк ===
        scroll = ScrollView(size_hint=(1, 0.55))
        self.list_layout = GridLayout(cols=1, size_hint_y=None, spacing=6)
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        self.update_list()
        scroll.add_widget(self.list_layout)
        layout.add_widget(scroll)

        # === Кнопки ===
        btns = BoxLayout(size_hint_y=None, height=50, spacing=6)
        add_btn = Button(text="➕", size_hint_x=0.2, background_color=(0.2, 0.7, 0.2, 1))
        clear_btn = Button(text="🧹 Очистить", size_hint_x=0.4, background_color=(0.8, 0.5, 0.1, 1))
        share_btn = Button(text="📤 Отправить", size_hint_x=0.4, background_color=(0.3, 0.6, 1, 1))
        add_btn.bind(on_press=self.add_row)
        clear_btn.bind(on_press=self.clear_all)
        share_btn.bind(on_press=self.share_anywhere)
        btns.add_widget(add_btn)
        btns.add_widget(clear_btn)
        btns.add_widget(share_btn)
        layout.add_widget(btns)

        # === Итог ===
        self.total_label = Label(text="", size_hint_y=None, height=60, halign="center")
        self.total_label.bind(size=self.total_label.setter("text_size"))
        layout.add_widget(self.total_label)
        self.update_total()

        # === История ===
        if self.history:
            layout.add_widget(Label(text="🗃️ Последние туры", size_hint_y=None, height=30, font_size=14))
            hist_scroll = ScrollView(size_hint=(1, 0.2))
            hist_grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
            hist_grid.bind(minimum_height=hist_grid.setter("height"))
            for tour in self.history[-5:]:  # последние 5
                btn = Button(
                    text=f"{tour['date']} — {tour['total']:,} ₽",
                    size_hint_y=None,
                    height=40,
                    font_size=13
                )
                btn.bind(on_press=lambda x, t=tour: self.load_from_history(t))
                hist_grid.add_widget(btn)
            hist_scroll.add_widget(hist_grid)
            layout.add_widget(hist_scroll)

        return layout

    def add_row(self, instance):
        row = BoxLayout(size_hint_y=None, height=45, spacing=6)
        desc = TextInput(hint_text="Куда / что", multiline=False, size_hint_x=0.7)
        amt = TextInput(hint_text="₽", input_filter="int", multiline=False, size_hint_x=0.25, halign="right")
        del_btn = Button(text="❌", size_hint_x=0.05, background_color=(0.9, 0.3, 0.3, 1))
        del_btn.bind(on_press=lambda x: self.remove_row(row))

        row.add_widget(desc)
        row.add_widget(amt)
        row.add_widget(del_btn)
        self.list_layout.add_widget(row)

        self.current["items"].append({"desc": "", "amount": 0})
        desc.bind(text=lambda i, t: self.update_item(row, "desc", t))
        amt.bind(text=lambda i, t: self.update_item(row, "amount", t or "0"))

    def remove_row(self, row):
        try:
            idx = len(self.list_layout.children) - 1 - self.list_layout.children.index(row)
            if 0 <= idx < len(self.current["items"]):
                self.list_layout.remove_widget(row)
                self.current["items"].pop(idx)
                self.update_total()
                self.save_current()
        except:
            pass

    def update_item(self, row, field, value):
        try:
            idx = len(self.list_layout.children) - 1 - self.list_layout.children.index(row)
            if idx < len(self.current["items"]):
                if field == "amount":
                    value = int(value) if value.isdigit() else 0
                self.current["items"][idx][field] = value
                self.update_total()
                self.save_current()
        except:
            pass

    def on_data_change(self, instance, value):
        self.current["date"] = self.date_input.text
        self.current["collected"] = int(self.collected_input.text) if self.collected_input.text.isdigit() else 0
        self.update_total()
        self.save_current()

    def update_total(self):
        total = sum(item["amount"] for item in self.current["items"])
        remain = max(0, total - self.current.get("collected", 0))
        self.total_label.text = (
            f"[b]Итого: {total:,} ₽[/b]\n"
            f"[color=#27ae60]Собрано: {self.current.get('collected', 0)}[/color] | "
            f"[color=#e74c3c]Осталось: {remain:,}[/color]"
        )
        self.total_label.markup = True

    def update_list(self):
        self.list_layout.clear_widgets()
        for item in self.current["items"]:
            row = BoxLayout(size_hint_y=None, height=45, spacing=6)
            desc = TextInput(text=item["desc"], hint_text="Куда / что", multiline=False, size_hint_x=0.7)
            amt = TextInput(text=str(item["amount"]), hint_text="₽", input_filter="int", multiline=False, size_hint_x=0.25, halign="right")
            del_btn = Button(text="❌", size_hint_x=0.05, background_color=(0.9, 0.3, 0.3, 1))
            del_btn.bind(on_press=lambda x, r=row: self.remove_row(r))
            row.add_widget(desc)
            row.add_widget(amt)
            row.add_widget(del_btn)
            self.list_layout.add_widget(row)
            desc.bind(text=lambda i, t, r=row: self.lazy_update(r, "desc", t))
            amt.bind(text=lambda i, t, r=row: self.lazy_update(r, "amount", t or "0"))

    def lazy_update(self, row, field, value):
        self.update_item(row, field, value)

    def save_current(self):
        self.data["current"] = self.current
        save_data(self.data)

    def clear_all(self, instance):
        self.current = {"date": "", "collected": 0, "items": []}
        self.date_input.text = ""
        self.collected_input.text = "0"
        self.update_list()
        self.update_total()
        self.save_current()

    def generate_text(self):
        lines = [f"📅 Дата: {self.current.get('date', '—')}", "", "📋 Программа:"]
        for item in self.current["items"]:
            d = item["desc"].strip()
            a = item["amount"]
            if d or a:
                line = f"• {d}" if d else "• —"
                if a:
                    line += f" — {a:,} ₽"
                lines.append(line)
        total = sum(i["amount"] for i in self.current["items"])
        lines.extend([
            "",
            f"💰 Итого: {total:,} ₽",
            f"✅ Собрано: {self.current.get('collected', 0)} ₽",
            f"❗ Осталось: {max(0, total - self.current.get('collected', 0)):,} ₽",
            "",
            "С уважением, Наталья 🌿"
        ])
        return "\n".join(lines)

    def share_anywhere(self, instance):
        text = self.generate_text()
        try:
            from android.permissions import request_permissions, Permission
            from jnius import autoclass

            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')

            # Сохраняем в историю перед отправкой
            total = sum(i["amount"] for i in self.current["items"])
            if total > 0:
                self.history.append({
                    "date": self.current.get("date", "—"),
                    "total": total,
                    "text": text,
                    "saved_at": datetime.now().isoformat()
                })
                # Оставляем только последние 5
                self.history = self.history[-5:]
                self.data["history"] = self.history
                save_data(self.data)

            # Отправка
            intent = Intent()
            intent.setAction(Intent.ACTION_SEND)
            intent.setType("text/plain")
            intent.putExtra(Intent.EXTRA_TEXT, String(text))
            intent.putExtra(Intent.EXTRA_SUBJECT, String(f"Тур {self.current.get('date', '')}"))

            chooser = Intent.createChooser(intent, String("Отправить как..."))
            PythonActivity.startActivity(chooser)

        except Exception as e:
            Clipboard.copy(text)
            Popup(
                title="📋 Скопировано",
                content=Label(text="Текст в буфере.\nВставьте в любой мессенджер.", halign="center"),
                size_hint=(0.8, 0.3)
            ).open()

    def load_from_history(self, tour):
        self.current = {
            "date": tour["date"],
            "collected": 0,
            "items": []
        }
        # Парсим текст, чтобы восстановить items (упрощённо)
        lines = tour["text"].split("\n")
        items = []
        for line in lines:
            if line.startswith("• ") and "—" in line:
                try:
                    part = line[2:].split(" — ")
                    desc = part[0].strip()
                    if len(part) > 1 and "₽" in part[-1]:
                        amt_str = part[-1].replace("₽", "").replace(",", "").strip()
                        amt = int(amt_str) if amt_str.isdigit() else 0
                    else:
                        amt = 0
                    items.append({"desc": desc, "amount": amt})
                except:
                    pass
        self.current["items"] = items
        self.date_input.text = self.current["date"]
        self.collected_input.text = "0"
        self.update_list()
        self.update_total()
        self.save_current()

if __name__ == "__main__":
    TourCounterApp().run()