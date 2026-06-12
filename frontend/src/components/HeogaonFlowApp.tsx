"use client";

import { useEffect, useState } from "react";
import { BottomBar } from "@/components/shell/BottomBar";
import { BrandLogo } from "@/components/shell/BrandLogo";
import { HistoryPanel } from "@/components/shell/HistoryPanel";
import { QuestionHeader } from "@/components/shell/QuestionHeader";
import { AnalysisLoadingScreen } from "@/components/views/AnalysisLoadingScreen";
import { FlowView } from "@/components/views/FlowView";
import { LandingScreen } from "@/components/views/LandingScreen";
import { sendTurn, startCase } from "@/lib/api";
import { primaryActionState, progressFor } from "@/lib/viewState";
import type { ApiEnvelope, DocumentItem, FlowActionId, TurnInput } from "@/types/flow";

const MIN_ANALYSIS_LOADING_MS = 950;

export function HeogaonFlowApp() {
  const [splashPhase, setSplashPhase] = useState<"visible" | "hiding" | "done">("visible");
  const [envelope, setEnvelope] = useState<ApiEnvelope | null>(null);
  const [caseId, setCaseId] = useState<string | null>(null);
  const [inputText, setInputText] = useState("");
  const [freeText, setFreeText] = useState("");
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [consultationText, setConsultationText] = useState("");
  const [activeDocument, setActiveDocument] = useState<DocumentItem | null>(null);
  const [historyOpen, setHistoryOpen] = useState(false);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");

  const view = envelope?.view;
  const showLanding = !view;
  const questionType = view?.type || "landing";
  const primary = view
    ? primaryActionState(view, selectedIds, freeText, consultationText, pending, envelope?.statePatch.completedDocumentIds || [])
    : null;
  const progress = progressFor(envelope?.caseState.progressStage || "intake");
  const ready = splashPhase === "done";

  useEffect(() => {
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const hideDelay = prefersReducedMotion ? 180 : 880;
    const doneDelay = prefersReducedMotion ? 260 : 1180;
    const hideTimer = window.setTimeout(() => setSplashPhase("hiding"), hideDelay);
    const doneTimer = window.setTimeout(() => setSplashPhase("done"), doneDelay);

    return () => {
      window.clearTimeout(hideTimer);
      window.clearTimeout(doneTimer);
    };
  }, []);

  async function run(task: () => Promise<void>) {
    setPending(true);
    setError("");
    try {
      await task();
    } catch (err) {
      setError(err instanceof Error ? err.message : "요청 처리에 실패했습니다.");
    } finally {
      setPending(false);
    }
  }

  async function handleStart() {
    const text = inputText.trim();
    if (!text || pending) return;

    await run(async () => {
      const [response] = await Promise.all([startCase(text), wait(MIN_ANALYSIS_LOADING_MS)]);
      setEnvelope(response);
      setCaseId(response.caseId);
      resetTransientInputs();
    });
  }

  async function handleTurn(input: TurnInput) {
    if (!caseId || pending) return;

    await run(async () => {
      const response = await sendTurn(caseId, input);
      setEnvelope(response);
      resetTransientInputs();
    });
  }

  function resetTransientInputs() {
    setSelectedIds([]);
    setFreeText("");
  }

  function resetCase() {
    setEnvelope(null);
    setCaseId(null);
    setInputText("");
    setSelectedIds([]);
    setFreeText("");
    setConsultationText("");
    setActiveDocument(null);
    setHistoryOpen(false);
    setError("");
  }

  function submitPrimary() {
    if (!view || !primary || primary.disabled) return;

    if (view.type === "slot_question") {
      handleTurn({
        type: "slot_answer",
        fieldKey: view.field,
        optionIds: selectedIds,
        text: freeText,
        value: freeText,
        unknown: selectedIds.includes("unknown"),
      });
      return;
    }

    if (view.type === "inquiry" && view.mode !== "channels") {
      handleTurn({ type: "consultation_answer", text: consultationText });
      return;
    }

    handleTurn({ type: "action", actionId: "primary" });
  }

  function submitAction(actionId: FlowActionId) {
    if (!caseId || pending) return;
    setHistoryOpen(false);
    handleTurn({ type: "action", actionId });
  }

  function submitUnknown() {
    if (!view || view.type !== "slot_question") return;

    handleTurn({
      type: "slot_answer",
      fieldKey: view.field,
      optionIds: ["unknown"],
      unknown: true,
    });
  }

  return (
    <>
      <main className={`app${ready ? " is-ready" : ""}`} id="app" aria-label="허가온" data-question-type={questionType}>
        {showLanding && pending ? (
          <AnalysisLoadingScreen />
        ) : showLanding ? (
          <LandingScreen inputText={inputText} pending={pending} onChange={setInputText} onStart={handleStart} />
        ) : (
          <section className="screen active" data-screen="question">
            <QuestionHeader progress={progress} onBack={resetCase} onHistory={() => setHistoryOpen(true)} />
            <div className="question-main">
              {error ? <p className="collect-status error-text">{error}</p> : null}
              <FlowView
                view={view}
                selectedIds={selectedIds}
                freeText={freeText}
                consultationText={consultationText}
                activeDocument={activeDocument}
                completedDocumentIds={envelope?.statePatch.completedDocumentIds || []}
                onSelectIds={setSelectedIds}
                onFreeText={setFreeText}
                onUnknown={submitUnknown}
                onConsultationText={setConsultationText}
                onChannel={(channel) => handleTurn({ type: "inquiry_channel", channel })}
                onToggleDocument={(documentId, completed) => handleTurn({ type: "document_toggle", documentId, completed })}
                onOpenDocument={setActiveDocument}
                onCloseDocument={() => setActiveDocument(null)}
                onDashboardContinue={submitPrimary}
                onDashboardAction={submitAction}
                dashboardContinueDisabled={!primary || primary.disabled}
              />
            </div>
            {primary ? (
              <BottomBar
                primary={primary}
                onPrimary={submitPrimary}
              />
            ) : null}
            <HistoryPanel open={historyOpen} envelope={envelope} onClose={() => setHistoryOpen(false)} onAction={submitAction} />
          </section>
        )}
      </main>
      {splashPhase !== "done" ? (
        <div className={`splash${splashPhase === "hiding" ? " is-hiding" : ""}`} role="status" aria-label="허가온 시작 화면">
          <BrandLogo />
        </div>
      ) : null}
    </>
  );
}

function wait(duration: number) {
  return new Promise((resolve) => window.setTimeout(resolve, duration));
}
