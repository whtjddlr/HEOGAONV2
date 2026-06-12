import { Icon, iconForDecision } from "@/components/common/Icon";
import type { DecisionBlock, DiagnosisView as DiagnosisViewModel } from "@/types/flow";

export function DiagnosisView({ view }: { view: DiagnosisViewModel }) {
  return (
    <>
      <section className="question-card">
        <h1 className="question-title">{view.title}</h1>
        <p className="question-sub">{view.headline}</p>
      </section>
      <div className="summary-view">
        <section className="summary-review">
          <div className="summary-review-title-row">
            <span aria-hidden="true"><Icon name="store" /></span>
            <h2 className="summary-review-title">검토할 신고</h2>
          </div>
          <ul className="confirmed-summary-list">
            {view.candidatePermits.map((permit) => (
              <li className="confirmed-summary-item" key={permit.name}>
                <span className="confirmed-summary-key">
                  <span className="confirmed-summary-icon" aria-hidden="true"><Icon name="search" /></span>
                  <span className="confirmed-summary-label">검토</span>
                </span>
                <span className="confirmed-summary-value">{permit.name}<br /><small>{permit.reason}</small></span>
              </li>
            ))}
          </ul>
        </section>
        {view.decisionBlocks.map((block) => (
          <DecisionBlockView block={block} key={block.type} />
        ))}
      </div>
    </>
  );
}

function DecisionBlockView({ block }: { block: DecisionBlock }) {
  return (
    <section className="summary-review">
      <div className="summary-review-title-row">
        <span aria-hidden="true"><Icon name={iconForDecision(block.type)} /></span>
        <h2 className="summary-review-title">{block.title}</h2>
      </div>
      <ul className="missing-summary-list">
        {block.items.map((item) => (
          <li className="missing-summary-item" key={item}>
            <span className="missing-summary-icon" aria-hidden="true"><Icon name={iconForDecision(block.type)} /></span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
