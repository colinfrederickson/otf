import * as TooltipPrimitive from '@radix-ui/react-tooltip';

export function Tooltip({ children, content }) {
  return (
    <TooltipPrimitive.Provider>
      <TooltipPrimitive.Root>
        <TooltipPrimitive.Trigger asChild>
          {children}
        </TooltipPrimitive.Trigger>
        <TooltipPrimitive.Portal>
          <TooltipPrimitive.Content
            className="rounded-lg bg-slate-800/80 px-3 py-2 text-sm text-slate-200 shadow-lg border border-slate-700/50 transition-opacity duration-200 ease-in-out"
            sideOffset={5}
          >
            {content}
            <TooltipPrimitive.Arrow className="fill-slate-800/80" />
          </TooltipPrimitive.Content>
        </TooltipPrimitive.Portal>
      </TooltipPrimitive.Root>
    </TooltipPrimitive.Provider>
  );
}
