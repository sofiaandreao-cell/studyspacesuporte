"""
Gerenciador de dados e persistência para a plataforma StudySpace.
Lida com leitura/escrita em JSON, cálculo de faltas, médias e simulação de notas.
"""

import json
import os
from datetime import datetime, date
from typing import Dict, List, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "student_data.json")

DEFAULT_DATA = {
    "settings": {
        "student_name": "Estudante Poli",
        "default_passing_grade": 5.0,
        "default_max_absence_pct": 30.0,  # Regra de 70% presença mínima na USP
        "academic_period": "2026/2"
    },
    "subjects": [
        {
            "id": "calc1",
            "name": "Cálculo Diferencial e Integral I",
            "code": "MAT2453",
            "professor": "Prof. Alano",
            "total_classes": 60,
            "absences": 6,
            "max_absence_pct": 30.0,
            "passing_grade": 5.0,
            "color": "#3B82F6",
            "evaluations": [
                {"name": "P1", "grade": 6.5, "weight": 2.0, "done": True},
                {"name": "P2", "grade": None, "weight": 3.0, "done": False},
                {"name": "P3", "grade": None, "weight": 3.0, "done": False}
            ]
        },
        {
            "id": "fis1",
            "name": "Física I - Mecânica",
            "code": "4302111",
            "professor": "Prof. Tanaka",
            "total_classes": 60,
            "absences": 14,
            "max_absence_pct": 30.0,
            "passing_grade": 5.0,
            "color": "#EF4444",
            "evaluations": [
                {"name": "P1", "grade": 4.2, "weight": 1.0, "done": True},
                {"name": "P2", "grade": None, "weight": 1.5, "done": False},
                {"name": "P3", "grade": None, "weight": 1.5, "done": False}
            ]
        },
        {
            "id": "alglinear",
            "name": "Álgebra Linear para Engenharia",
            "code": "MAT2457",
            "professor": "Profa. Beatriz",
            "total_classes": 45,
            "absences": 3,
            "max_absence_pct": 30.0,
            "passing_grade": 5.0,
            "color": "#10B981",
            "evaluations": [
                {"name": "P1", "grade": 8.0, "weight": 1.0, "done": True},
                {"name": "P2", "grade": None, "weight": 1.0, "done": False}
            ]
        },
        {
            "id": "intro_comp",
            "name": "Introdução à Computação (Python)",
            "code": "MAC2166",
            "professor": "Prof. Miranda",
            "total_classes": 60,
            "absences": 2,
            "max_absence_pct": 30.0,
            "passing_grade": 5.0,
            "color": "#8B5CF6",
            "evaluations": [
                {"name": "EP1 (Exercício Prático)", "grade": 9.5, "weight": 1.0, "done": True},
                {"name": "P1", "grade": 7.0, "weight": 2.0, "done": True},
                {"name": "EP2", "grade": None, "weight": 1.0, "done": False},
                {"name": "P2", "grade": None, "weight": 2.0, "done": False}
            ]
        }
    ],
    "exams": [
        {
            "id": "exam_1",
            "subject_id": "calc1",
            "title": "P2 - Cálculo I",
            "date": "2026-09-15",
            "time": "14:00",
            "room": "Biênio - Sala 12",
            "topics": "Derivadas, Regra da Cadeia, Taxas Relacionadas e Máximos/Mínimos",
            "weight": 3.0,
            "importance": "Alta"
        },
        {
            "id": "exam_2",
            "subject_id": "fis1",
            "title": "P2 - Física I",
            "date": "2026-09-18",
            "time": "10:00",
            "room": "Auditório Mecânica",
            "topics": "Leis de Newton, Atrito, Trabalho, Energia Cinética e Potencial",
            "weight": 1.5,
            "importance": "Crítica"
        },
        {
            "id": "exam_3",
            "subject_id": "intro_comp",
            "title": "Entrega EP2 - Algoritmos de Grafos",
            "date": "2026-09-22",
            "time": "23:59",
            "room": "e-Disciplinas (Online)",
            "topics": "Listas encadeadas, Recursão e Busca em Grafos",
            "weight": 1.0,
            "importance": "Média"
        },
        {
            "id": "exam_4",
            "subject_id": "alglinear",
            "title": "P2 - Álgebra Linear",
            "date": "2026-09-29",
            "time": "08:00",
            "room": "Prédio da Elétrica - C1-04",
            "topics": "Espaços Vetoriais, Bases, Transformações Lineares e Autovalores",
            "weight": 1.0,
            "importance": "Alta"
        }
    ],
    "tasks": [
        {"id": "t1", "subject_id": "calc1", "text": "Resolver lista 4 de Derivadas e Taxas Relacionadas", "done": False, "priority": "Alta"},
        {"id": "t2", "subject_id": "fis1", "text": "Revisar exercícios da Prova Antiga 2025 de Física I", "done": True, "priority": "Alta"},
        {"id": "t3", "subject_id": "intro_comp", "text": "Estruturar as funções principais do EP2 em Python", "done": False, "priority": "Média"},
        {"id": "t4", "subject_id": "alglinear", "text": "Assistir vídeo de revisão de Transformações Lineares", "done": False, "priority": "Baixa"}
    ]
}


class DataManager:
    """Controlador de dados da aplicação com persistência em arquivo JSON."""

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(DATA_FILE):
            self.save_all(DEFAULT_DATA)

    def load_all(self) -> Dict[str, Any]:
        """Carrega todos os dados do arquivo JSON."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_DATA.copy()

    def save_all(self, data: Dict[str, Any]) -> bool:
        """Salva todos os dados no arquivo JSON."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False

    def reset_to_defaults(self) -> Dict[str, Any]:
        """Restaura os dados padrão de exemplo."""
        self.save_all(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    # --- CONFIGURAÇÕES GERAIS ---
    def get_settings(self) -> Dict[str, Any]:
        data = self.load_all()
        return data.get("settings", {
            "student_name": "Estudante",
            "institution_name": "Minha Faculdade / Colégio",
            "default_passing_grade": 5.0,
            "default_max_absence_pct": 25.0,
            "academic_period": "2026/2"
        })

    def update_settings(self, new_settings: Dict[str, Any]) -> bool:
        data = self.load_all()
        if "settings" not in data:
            data["settings"] = {}
        data["settings"].update(new_settings)
        return self.save_all(data)

    def clear_all_subjects(self) -> bool:
        """Limpa todas as matérias para o usuário começar do zero."""
        data = self.load_all()
        data["subjects"] = []
        data["exams"] = []
        data["tasks"] = []
        return self.save_all(data)

    def load_preset(self, preset_name: str) -> bool:
        """Carrega um modelo pré-definido de matérias ou limpa para personalização."""
        if preset_name == "vazio":
            return self.clear_all_subjects()
        elif preset_name == "geral":
            data = self.load_all()
            data["subjects"] = [
                {
                    "id": "mat1",
                    "name": "Matemática Aplicada",
                    "code": "MAT101",
                    "professor": "Prof. Silva",
                    "total_classes": 60,
                    "absences": 2,
                    "max_absence_pct": 25.0,
                    "passing_grade": 6.0,
                    "color": "#3B82F6",
                    "evaluations": [
                        {"name": "Prova 1", "grade": 7.5, "weight": 1.0, "done": True},
                        {"name": "Prova 2", "grade": None, "weight": 1.0, "done": False}
                    ]
                },
                {
                    "id": "com1",
                    "name": "Comunicação e Redação",
                    "code": "LET102",
                    "professor": "Profa. Helena",
                    "total_classes": 40,
                    "absences": 4,
                    "max_absence_pct": 25.0,
                    "passing_grade": 6.0,
                    "color": "#10B981",
                    "evaluations": [
                        {"name": "Artigo / Resenha", "grade": 8.0, "weight": 1.0, "done": True},
                        {"name": "Apresentação Final", "grade": None, "weight": 1.0, "done": False}
                    ]
                },
                {
                    "id": "met1",
                    "name": "Metodologia da Pesquisa",
                    "code": "MET103",
                    "professor": "Prof. Carlos",
                    "total_classes": 40,
                    "absences": 1,
                    "max_absence_pct": 25.0,
                    "passing_grade": 6.0,
                    "color": "#8B5CF6",
                    "evaluations": [
                        {"name": "Projeto de Pesquisa", "grade": None, "weight": 1.0, "done": False}
                    ]
                }
            ]
            data["exams"] = [
                {
                    "id": "exam_g1",
                    "subject_id": "mat1",
                    "title": "Prova 2 de Matemática",
                    "date": "2026-09-20",
                    "time": "10:00",
                    "room": "Sala 101",
                    "topics": "Estatística e Probabilidade",
                    "weight": 1.0,
                    "importance": "Alta"
                }
            ]
            data["tasks"] = [
                {"id": "tg1", "subject_id": "mat1", "text": "Revisar exercícios do capítulo 3", "done": False, "priority": "Média"}
            ]
            return self.save_all(data)
        elif preset_name == "engenharia":
            self.reset_to_defaults()
            return True
        return False

    # --- DISCIPLINAS ---
    def get_subjects(self) -> List[Dict[str, Any]]:
        return self.load_all().get("subjects", [])

    def get_subject_by_id(self, subject_id: str) -> Optional[Dict[str, Any]]:
        for s in self.get_subjects():
            if s["id"] == subject_id:
                return s
        return None

    def add_subject(self, subject: Dict[str, Any]) -> bool:
        data = self.load_all()
        data["subjects"].append(subject)
        return self.save_all(data)

    def update_subject(self, subject_id: str, updated_fields: Dict[str, Any]) -> bool:
        data = self.load_all()
        for i, s in enumerate(data["subjects"]):
            if s["id"] == subject_id:
                data["subjects"][i].update(updated_fields)
                return self.save_all(data)
        return False

    def delete_subject(self, subject_id: str) -> bool:
        data = self.load_all()
        data["subjects"] = [s for s in data["subjects"] if s["id"] != subject_id]
        # Remover também provas e tarefas vinculadas
        data["exams"] = [e for e in data.get("exams", []) if e.get("subject_id") != subject_id]
        data["tasks"] = [t for t in data.get("tasks", []) if t.get("subject_id") != subject_id]
        return self.save_all(data)

    # --- FALTAS ---
    def modify_absences(self, subject_id: str, delta: int) -> int:
        """Altera as faltas de uma disciplina somando delta (+1, -1, etc)."""
        data = self.load_all()
        new_val = 0
        for s in data["subjects"]:
            if s["id"] == subject_id:
                s["absences"] = max(0, min(s["total_classes"], s["absences"] + delta))
                new_val = s["absences"]
                break
        self.save_all(data)
        return new_val

    def set_absences(self, subject_id: str, count: int) -> bool:
        data = self.load_all()
        for s in data["subjects"]:
            if s["id"] == subject_id:
                s["absences"] = max(0, min(s["total_classes"], count))
                break
        return self.save_all(data)

    def get_attendance_stats(self, subject: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula estatísticas detalhadas de faltas e limite de reprovação."""
        total = subject.get("total_classes", 60)
        absences = subject.get("absences", 0)
        max_pct = subject.get("max_absence_pct", 30.0)

        max_allowed_absences = int((max_pct / 100.0) * total)
        remaining_allowed = max_allowed_absences - absences
        absence_rate = (absences / total * 100.0) if total > 0 else 0.0
        attendance_rate = 100.0 - absence_rate

        # Status:
        # 'safe' (< 60% do limite de faltas atingido)
        # 'warning' (>= 60% e < 90%)
        # 'danger' (>= 90% e <= 100%)
        # 'failed' (> 100%)
        usage_pct = (absences / max_allowed_absences * 100.0) if max_allowed_absences > 0 else 0.0

        if absences > max_allowed_absences:
            status = "failed"
            status_text = "Reprovado por Frequência"
            status_color = "#DC2626"
        elif usage_pct >= 80:
            status = "danger"
            status_text = "Risco Iminente de Reprovação"
            status_color = "#EF4444"
        elif usage_pct >= 50:
            status = "warning"
            status_text = "Atenção com Faltas"
            status_color = "#F59E0B"
        else:
            status = "safe"
            status_text = "Frequência Segura"
            status_color = "#10B981"

        return {
            "total_classes": total,
            "absences": absences,
            "max_allowed_absences": max_allowed_absences,
            "remaining_allowed": max(0, remaining_allowed),
            "is_exceeded": absences > max_allowed_absences,
            "excess_absences": max(0, absences - max_allowed_absences),
            "absence_rate": round(absence_rate, 1),
            "attendance_rate": round(attendance_rate, 1),
            "usage_pct": round(usage_pct, 1),
            "status": status,
            "status_text": status_text,
            "status_color": status_color
        }

    # --- NOTAS E MÉDIAS ---
    def calculate_grade_stats(self, subject: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula média atual, peso restante e quanto precisa tirar nas próximas provas."""
        evals = subject.get("evaluations", [])
        passing_grade = subject.get("passing_grade", 5.0)

        total_weight = sum(e.get("weight", 1.0) for e in evals)
        if total_weight == 0:
            total_weight = 1.0

        done_weight = 0.0
        done_weighted_sum = 0.0
        pending_weight = 0.0
        pending_evals = []

        for e in evals:
            w = e.get("weight", 1.0)
            g = e.get("grade")
            if g is not None and e.get("done", False):
                done_weight += w
                done_weighted_sum += (g * w)
            else:
                pending_weight += w
                pending_evals.append(e)

        # Média atual das já realizadas
        current_avg = (done_weighted_sum / done_weight) if done_weight > 0 else 0.0
        
        # Média ponderada global considerando 0 para as restantes
        projected_current = (done_weighted_sum / total_weight)

        # Quanto precisa tirar nas pendentes:
        # passing_grade = (done_weighted_sum + grade_needed * pending_weight) / total_weight
        # grade_needed * pending_weight = passing_grade * total_weight - done_weighted_sum
        needed_sum = (passing_grade * total_weight) - done_weighted_sum

        if pending_weight > 0:
            grade_needed_each = needed_sum / pending_weight
            grade_needed_each = round(grade_needed_each, 2)
        else:
            grade_needed_each = None

        is_already_passed = projected_current >= passing_grade
        is_impossible = (grade_needed_each is not None and grade_needed_each > 10.0)

        return {
            "current_avg": round(current_avg, 2),
            "projected_current": round(projected_current, 2),
            "passing_grade": passing_grade,
            "total_weight": round(total_weight, 2),
            "done_weight": round(done_weight, 2),
            "pending_weight": round(pending_weight, 2),
            "pending_count": len(pending_evals),
            "grade_needed_each": grade_needed_each,
            "is_already_passed": is_already_passed,
            "is_impossible": is_impossible,
            "pending_evals": pending_evals
        }

    # --- PROVAS E CALENDÁRIO ---
    def get_exams(self) -> List[Dict[str, Any]]:
        exams = self.load_all().get("exams", [])
        # Ordenar por data
        def sort_key(ex):
            d = ex.get("date", "9999-12-31")
            t = ex.get("time", "00:00")
            return f"{d} {t}"
        return sorted(exams, key=sort_key)

    def add_exam(self, exam: Dict[str, Any]) -> bool:
        data = self.load_all()
        data["exams"].append(exam)
        return self.save_all(data)

    def update_exam(self, exam_id: str, updated_fields: Dict[str, Any]) -> bool:
        data = self.load_all()
        for i, ex in enumerate(data["exams"]):
            if ex["id"] == exam_id:
                data["exams"][i].update(updated_fields)
                return self.save_all(data)
        return False

    def delete_exam(self, exam_id: str) -> bool:
        data = self.load_all()
        data["exams"] = [e for e in data.get("exams", []) if e["id"] != exam_id]
        return self.save_all(data)

    # --- TAREFAS / CRONOGRAMA ---
    def get_tasks(self) -> List[Dict[str, Any]]:
        return self.load_all().get("tasks", [])

    def add_task(self, task: Dict[str, Any]) -> bool:
        data = self.load_all()
        data["tasks"].append(task)
        return self.save_all(data)

    def toggle_task(self, task_id: str) -> bool:
        data = self.load_all()
        for t in data["tasks"]:
            if t["id"] == task_id:
                t["done"] = not t.get("done", False)
                break
        return self.save_all(data)

    def delete_task(self, task_id: str) -> bool:
        data = self.load_all()
        data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
        return self.save_all(data)